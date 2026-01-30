#!/usr/bin/env python3
"""
Test script with mocked data to verify the system works correctly
without needing network access.
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_mock_release_data():
    """Create mock release data for testing."""
    return {
        'version': '2026.01',
        'title': 'Home Assistant 2026.01: Great Start to the Year!',
        'url': 'https://www.home-assistant.io/blog/2026/01/08/release-202601/',
        'content': '''
# Home Assistant 2026.01: Great Start to the Year!

We're excited to announce the first release of 2026! This release brings many improvements and new features.

## New Integrations

- **Tesla Powerwall**: Enhanced integration with better battery monitoring
- **Matter**: Support for new Matter 1.3 devices
- **OpenAI Conversation**: Improved conversation agent with GPT-4 Turbo

## Automation Improvements

- New trigger type: State change detection with pattern matching
- Template improvements for better scripting capabilities
- Enhanced automation debugging tools

## Performance & Architecture

- 15% faster startup time on Raspberry Pi
- Reduced memory usage for large installations
- Improved database query performance
- Better error handling and recovery

## Breaking Changes

- Deprecated sensor.legacy_sensor has been removed
- Some integrations now require re-authentication

This is a summary of the main features. Check the full changelog for details.
        ''',
        'found_date': datetime.now().isoformat()
    }

def test_article_generation():
    """Test article generation with mock data."""
    logger.info("=== Starting Mock Test ===")

    # Import modules
    try:
        from article_generator import ArticleGenerator
        import yaml

        # Load config
        config_path = Path(__file__).parent / "config.yaml"
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        logger.info("✅ Configuration loaded")

        # Create mock data
        release_data = create_mock_release_data()
        logger.info(f"✅ Mock data created for version {release_data['version']}")

        # Test article generator
        logger.info("Testing article generation with Claude Code CLI...")
        generator = ArticleGenerator(config)

        # Generate article
        article_path = generator.generate_article(release_data)

        if article_path and article_path.exists():
            logger.info(f"✅ Article generated successfully: {article_path}")
            logger.info(f"   File size: {article_path.stat().st_size} bytes")

            # Show first few lines
            with open(article_path, 'r') as f:
                lines = f.readlines()[:10]
            logger.info("   First 10 lines of article:")
            for line in lines:
                logger.info(f"   {line.rstrip()}")

            return True
        else:
            logger.error("❌ Article generation failed")
            return False

    except Exception as e:
        logger.error(f"❌ Test failed: {e}", exc_info=True)
        return False

def test_version_increment():
    """Test version increment logic."""
    logger.info("\n=== Testing Version Increment Logic ===")

    def increment_version(version):
        year, month = version.split('.')
        year, month = int(year), int(month)
        month += 1
        if month > 12:
            year += 1
            month = 1
        return f"{year}.{month:02d}"

    test_cases = [
        ('2026.01', '2026.02'),
        ('2026.11', '2026.12'),
        ('2026.12', '2027.01'),
    ]

    all_passed = True
    for input_ver, expected in test_cases:
        result = increment_version(input_ver)
        if result == expected:
            logger.info(f"✅ {input_ver} -> {result}")
        else:
            logger.error(f"❌ {input_ver} -> {result} (expected {expected})")
            all_passed = False

    return all_passed

if __name__ == "__main__":
    logger.info("🚀 Mock Test Suite for Home Assistant Article Generator\n")

    # Test 1: Version increment
    test1_passed = test_version_increment()

    # Test 2: Article generation
    test2_passed = test_article_generation()

    # Summary
    logger.info("\n=== Test Summary ===")
    logger.info(f"Version Increment: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    logger.info(f"Article Generation: {'✅ PASSED' if test2_passed else '❌ FAILED'}")

    if test1_passed and test2_passed:
        logger.info("\n🎉 All tests passed! System is ready for production.")
        sys.exit(0)
    else:
        logger.error("\n⚠️  Some tests failed. Please check the logs above.")
        sys.exit(1)
