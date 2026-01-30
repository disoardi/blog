#!/usr/bin/env python3
"""
Test script for Home Assistant Release Monitor system.
Verifies all components are working correctly.
"""

import os
import sys
import logging
from pathlib import Path
import yaml

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_imports():
    """Test that all required modules can be imported."""
    logger.info("Testing imports...")
    try:
        import requests
        import yaml
        import anthropic
        from bs4 import BeautifulSoup
        logger.info("✓ All required modules imported successfully")
        return True
    except ImportError as e:
        logger.error(f"✗ Import error: {e}")
        return False


def test_config():
    """Test that config file exists and is valid."""
    logger.info("Testing configuration...")
    try:
        config_path = Path("automation/config.yaml")
        if not config_path.exists():
            logger.error("✗ config.yaml not found")
            return False

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Check required keys
        required_keys = ['blog', 'monitoring', 'claude', 'git']
        for key in required_keys:
            if key not in config:
                logger.error(f"✗ Missing required config key: {key}")
                return False

        logger.info("✓ Configuration file is valid")
        return True
    except Exception as e:
        logger.error(f"✗ Config error: {e}")
        return False


def test_env():
    """Test that environment variables are set."""
    logger.info("Testing environment variables...")

    # Try loading from .env file
    try:
        from dotenv import load_dotenv
        load_dotenv('automation/.env')
    except:
        pass

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        logger.warning("⚠ ANTHROPIC_API_KEY not set")
        logger.warning("  Set it in .env file or as environment variable")
        return False

    if api_key == "your_api_key_here":
        logger.error("✗ ANTHROPIC_API_KEY still has default value")
        logger.error("  Please update .env with your actual API key")
        return False

    logger.info("✓ ANTHROPIC_API_KEY is set")
    return True


def test_git():
    """Test git repository status."""
    logger.info("Testing git repository...")
    try:
        import subprocess

        result = subprocess.run(
            ['git', 'rev-parse', '--git-dir'],
            cwd='..',
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            logger.warning("⚠ Not in a git repository")
            return False

        # Get current branch
        branch_result = subprocess.run(
            ['git', 'branch', '--show-current'],
            cwd='..',
            capture_output=True,
            text=True
        )
        current_branch = branch_result.stdout.strip()

        logger.info(f"✓ Git repository detected (branch: {current_branch})")
        return True

    except Exception as e:
        logger.error(f"✗ Git test failed: {e}")
        return False


def test_directories():
    """Test that required directories exist."""
    logger.info("Testing directory structure...")

    required_dirs = [
        Path('automation/logs'),
        Path('automation/temp'),
        Path('Post'),
        Path('img')
    ]

    all_exist = True
    for dir_path in required_dirs:
        if not dir_path.exists():
            logger.warning(f"⚠ Directory does not exist: {dir_path}")
            logger.info(f"  Creating: {dir_path}")
            dir_path.mkdir(parents=True, exist_ok=True)
        else:
            logger.info(f"✓ Directory exists: {dir_path}")

    return all_exist


def test_ha_blog_access():
    """Test access to Home Assistant blog."""
    logger.info("Testing Home Assistant blog access...")
    try:
        import requests

        url = "https://www.home-assistant.io/blog/categories/core/"
        response = requests.get(
            url,
            headers={'User-Agent': 'Mozilla/5.0'},
            timeout=10
        )

        if response.status_code == 200:
            logger.info("✓ Successfully accessed Home Assistant blog")
            return True
        else:
            logger.error(f"✗ HTTP {response.status_code} when accessing blog")
            return False

    except Exception as e:
        logger.error(f"✗ Failed to access blog: {e}")
        return False


def test_anthropic_api():
    """Test Anthropic API connection."""
    logger.info("Testing Anthropic API connection...")

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key or api_key == "your_api_key_here":
        logger.warning("⚠ Skipping API test (no valid key)")
        return False

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)

        # Make a simple test call
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=100,
            messages=[
                {"role": "user", "content": "Say 'API test successful' and nothing else."}
            ]
        )

        response_text = message.content[0].text
        logger.info(f"✓ API response: {response_text}")
        return True

    except anthropic.AuthenticationError:
        logger.error("✗ Invalid API key")
        return False
    except Exception as e:
        logger.error(f"✗ API test failed: {e}")
        return False


def test_module_imports():
    """Test that custom modules can be imported."""
    logger.info("Testing custom module imports...")
    try:
        sys.path.insert(0, 'automation')

        from ha_release_monitor import HomeAssistantReleaseMonitor
        from article_generator import ArticleGenerator
        from git_manager import GitManager

        logger.info("✓ All custom modules imported successfully")
        return True

    except ImportError as e:
        logger.error(f"✗ Module import error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Home Assistant Release Monitor - System Test")
    print("=" * 60)
    print()

    tests = [
        ("Python Dependencies", test_imports),
        ("Configuration File", test_config),
        ("Environment Variables", test_env),
        ("Directory Structure", test_directories),
        ("Git Repository", test_git),
        ("HA Blog Access", test_ha_blog_access),
        ("Custom Modules", test_module_imports),
        ("Anthropic API", test_anthropic_api),
    ]

    results = {}
    for test_name, test_func in tests:
        print(f"\n[{test_name}]")
        try:
            results[test_name] = test_func()
        except Exception as e:
            logger.error(f"✗ Test crashed: {e}")
            results[test_name] = False
        print()

    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:10} | {test_name}")

    print()
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! System is ready to use.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
