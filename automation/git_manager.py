#!/usr/bin/env python3
"""
Git Manager Module
Handles automatic git commits and pushes for generated articles.
"""

import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class GitManager:
    """Manage git operations for blog automation."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize git manager."""
        self.config = config
        self.blog_root = Path(config['blog']['root_path'])
        self.auto_push = config['git'].get('auto_push', True)
        self.branch = config['git'].get('branch', 'main')

    def _run_git_command(self, cmd: list, check: bool = True) -> subprocess.CompletedProcess:
        """
        Run a git command in the blog repository.
        """
        try:
            result = subprocess.run(
                cmd,
                cwd=self.blog_root,
                capture_output=True,
                text=True,
                check=check
            )
            return result
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {' '.join(cmd)}")
            logger.error(f"Error output: {e.stderr}")
            raise

    def commit_and_push(self, article_path: Path, additional_files: list = None) -> bool:
        """
        Commit and push the generated article.

        Args:
            article_path: Path to the generated article
            additional_files: Optional list of additional files to commit (e.g., images)

        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert to relative path from blog root
            rel_article_path = article_path.relative_to(self.blog_root)

            logger.info(f"Preparing to commit: {rel_article_path}")

            # Check git status
            status = self._run_git_command(['git', 'status', '--porcelain'])
            if not status.stdout.strip():
                logger.warning("No changes to commit")
                return False

            # Add the article file
            self._run_git_command(['git', 'add', str(rel_article_path)])
            logger.info(f"Added file: {rel_article_path}")

            # Add Hugo generated files (public/ directory)
            public_dir = self.blog_root / 'public'
            if public_dir.exists():
                try:
                    self._run_git_command(['git', 'add', 'public/'])
                    logger.info("Added Hugo generated files (public/)")
                except:
                    logger.warning("Could not add public/ directory - may not be tracked")

            # Add any additional files (like images)
            if additional_files:
                for file_path in additional_files:
                    rel_path = file_path.relative_to(self.blog_root)
                    self._run_git_command(['git', 'add', str(rel_path)])
                    logger.info(f"Added file: {rel_path}")

            # Extract article title from filename
            filename = article_path.stem
            # Format: yyyyMMdd_title_vXX.Y
            parts = filename.split('_')
            if len(parts) >= 2:
                title = ' '.join(parts[1:-1]).replace('-', ' ').title()
            else:
                title = filename

            # Create commit message
            commit_msg = f"""Nuovo articolo: {title}

Articolo generato automaticamente sulla release di Home Assistant.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"""

            # Commit
            self._run_git_command([
                'git', 'commit', '-m', commit_msg
            ])
            logger.info("Commit created successfully")

            # Push if enabled
            if self.auto_push:
                logger.info(f"Pushing to origin/{self.branch}...")
                self._run_git_command([
                    'git', 'push', 'origin', self.branch
                ])
                logger.info("Push completed successfully")
            else:
                logger.info("Auto-push disabled, commit created locally only")

            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Git operation failed: {e}", exc_info=True)
            return False
        except Exception as e:
            logger.error(f"Error in commit_and_push: {e}", exc_info=True)
            return False

    def check_repo_status(self) -> Dict[str, Any]:
        """
        Check the status of the git repository.

        Returns:
            Dictionary with repo status information
        """
        try:
            # Check if we're in a git repo
            self._run_git_command(['git', 'rev-parse', '--git-dir'])

            # Get current branch
            branch_result = self._run_git_command(['git', 'branch', '--show-current'])
            current_branch = branch_result.stdout.strip()

            # Get status
            status_result = self._run_git_command(['git', 'status', '--porcelain'])
            has_changes = bool(status_result.stdout.strip())

            # Check if there are unpushed commits
            try:
                unpushed = self._run_git_command(
                    ['git', 'log', f'origin/{current_branch}..HEAD', '--oneline'],
                    check=False
                )
                has_unpushed = bool(unpushed.stdout.strip())
            except:
                has_unpushed = False

            return {
                'is_repo': True,
                'current_branch': current_branch,
                'has_changes': has_changes,
                'has_unpushed_commits': has_unpushed
            }

        except subprocess.CalledProcessError:
            return {
                'is_repo': False,
                'error': 'Not a git repository'
            }

    def pull_latest(self) -> bool:
        """
        Pull latest changes from remote.

        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("Pulling latest changes from remote...")
            self._run_git_command(['git', 'pull', 'origin', self.branch])
            logger.info("Pull completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to pull latest changes: {e}")
            return False


if __name__ == "__main__":
    # Testing
    import yaml
    import sys

    logging.basicConfig(level=logging.INFO)

    with open('automation/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    manager = GitManager(config)

    # Check status
    status = manager.check_repo_status()
    print(f"Repository status: {status}")

    if len(sys.argv) > 1 and sys.argv[1] == 'status':
        sys.exit(0)

    # Test commit (if file provided)
    if len(sys.argv) > 2 and sys.argv[1] == 'commit':
        test_file = Path(sys.argv[2])
        if test_file.exists():
            success = manager.commit_and_push(test_file)
            print(f"Commit {'successful' if success else 'failed'}")
        else:
            print(f"File not found: {test_file}")
            sys.exit(1)
