#!/usr/bin/env python3
"""
Home Assistant Release Monitor and Article Generator
Monitors Home Assistant releases and automatically generates blog articles
when new versions are detected.
"""

import os
import sys
import json
import logging
import requests
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import yaml
from bs4 import BeautifulSoup

# Setup logging
# Get script directory to handle relative paths correctly
SCRIPT_DIR = Path(__file__).parent
LOG_DIR = SCRIPT_DIR / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'ha_monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class HomeAssistantReleaseMonitor:
    """Monitor Home Assistant releases and trigger article generation."""

    def __init__(self, config_path: str = None):
        """Initialize the monitor with configuration."""
        if config_path is None:
            # Use path relative to script location
            config_path = Path(__file__).parent / "config.yaml"
        self.config = self._load_config(config_path)
        self.blog_root = Path(self.config['blog']['root_path'])

        # Handle state file path - make it absolute if relative
        state_file = self.config['monitoring']['state_file']
        self.state_file = Path(state_file)
        if not self.state_file.is_absolute():
            # Make it relative to script directory
            self.state_file = Path(__file__).parent / state_file.replace('automation/', '')

        self.target_version = self.config['monitoring']['target_version']
        self.ha_blog_url = self.config['monitoring']['ha_blog_url']

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _load_state(self) -> Dict[str, Any]:
        """Load the current state from file."""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {"last_checked_version": None, "article_generated": False}

    def _save_state(self, state: Dict[str, Any]) -> None:
        """Save the current state to file."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def _normalize_version(self, version: str) -> str:
        """
        Normalize version string to handle both formats: 2026.01 and 2026.1
        Returns the format without leading zeros in month: 2026.1
        """
        try:
            year, month = version.split('.')
            return f"{year}.{int(month)}"
        except:
            return version

    def check_for_new_release(self) -> Optional[Dict[str, Any]]:
        """
        Check Home Assistant blog for new releases.
        Returns release info if target version is found, None otherwise.
        """
        logger.info(f"Checking for Home Assistant release {self.target_version}")

        try:
            response = requests.get(
                self.ha_blog_url,
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=30
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Normalize target version for comparison (2026.01 -> 2026.1)
            normalized_target = self._normalize_version(self.target_version)
            logger.info(f"Searching for version {self.target_version} (normalized: {normalized_target})")

            # Strategy: Look through ALL links on the page for release announcements
            # Release URLs typically look like: /blog/2026/01/07/release-20261/
            all_links = soup.find_all('a', href=True)
            logger.info(f"Scanning {len(all_links)} links on page")

            for link in all_links:
                link_text = link.get_text().strip()
                link_href = link.get('href', '')

                # Check if this link is a release announcement
                # Look for version in both text and URL
                if (normalized_target in link_text or self.target_version in link_text) or \
                   (normalized_target.replace('.', '') in link_href):  # e.g., "20261" in URL

                    logger.info(f"Found potential release: '{link_text}' -> {link_href}")

                    # Build full URL
                    article_url = link_href
                    if not article_url.startswith('http'):
                        article_url = f"https://www.home-assistant.io{article_url}"

                    # Verify it's actually a release announcement (contains /release- or /blog/)
                    if '/blog/' in article_url or '/release-' in article_url:
                        logger.info(f"✅ Confirmed release announcement: {link_text}")

                        return {
                            'version': self.target_version,
                            'title': link_text if link_text else f"Home Assistant {self.target_version}",
                            'url': article_url,
                            'found_date': datetime.now().isoformat()
                        }

            logger.info(f"Target version {self.target_version} not yet released")
            return None

        except Exception as e:
            logger.error(f"Error checking for releases: {e}", exc_info=True)
            return None

    def fetch_release_content(self, release_info: Dict[str, Any]) -> Optional[str]:
        """
        Fetch the full content of the release announcement.
        """
        if not release_info.get('url'):
            logger.warning("No URL provided for release content")
            return None

        try:
            logger.info(f"Fetching release content from {release_info['url']}")
            response = requests.get(
                release_info['url'],
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=30
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the main content area
            content = soup.find('article') or soup.find('div', class_='content')

            if content:
                # Extract text while preserving some structure
                return content.get_text(separator='\n', strip=True)

            logger.warning("Could not find main content in release page")
            return None

        except Exception as e:
            logger.error(f"Error fetching release content: {e}", exc_info=True)
            return None

    def run(self) -> bool:
        """
        Main execution loop.
        Returns True if article was generated, False otherwise.
        """
        logger.info("Starting Home Assistant Release Monitor")

        # Load current state
        state = self._load_state()

        # Check if we already generated an article for this version
        if state.get('article_generated') and state.get('last_checked_version') == self.target_version:
            logger.info(f"Article already generated for version {self.target_version}")
            return False

        # Check for new release
        release_info = self.check_for_new_release()

        if not release_info:
            logger.info("No new release found")
            return False

        # Fetch release content
        release_content = self.fetch_release_content(release_info)

        if not release_content:
            logger.warning("Could not fetch release content, will retry next time")
            return False

        # Store release info for article generator
        release_data = {
            **release_info,
            'content': release_content
        }

        # Save release data to temp file for article generator
        temp_file = Path(__file__).parent / 'temp' / 'release_data.json'
        temp_file.parent.mkdir(parents=True, exist_ok=True)
        with open(temp_file, 'w') as f:
            json.dump(release_data, f, indent=2)

        logger.info("Release data prepared for article generation")

        # Import and run article generator
        try:
            from article_generator import ArticleGenerator

            generator = ArticleGenerator(self.config)
            article_path = generator.generate_article(release_data)

            if article_path:
                logger.info(f"✅ Article generated successfully!")
                logger.info(f"📄 Location: {article_path}")
                logger.info(f"")
                logger.info(f"Next steps:")
                logger.info(f"1. Review the article: {article_path}")
                logger.info(f"2. Make any edits if needed")
                logger.info(f"3. Build with Hugo: hugo")
                logger.info(f"4. Commit and push manually when ready")

                # Update state to mark this version as processed
                state['last_checked_version'] = self.target_version
                state['article_generated'] = True
                state['article_path'] = str(article_path)
                state['generation_date'] = datetime.now().isoformat()
                self._save_state(state)

                return True
            else:
                logger.error("Article generation failed")
                return False

        except Exception as e:
            logger.error(f"Error in article generation pipeline: {e}", exc_info=True)
            return False


def main():
    """Main entry point."""
    try:
        monitor = HomeAssistantReleaseMonitor()
        success = monitor.run()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
