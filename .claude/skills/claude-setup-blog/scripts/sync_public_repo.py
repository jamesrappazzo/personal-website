#!/usr/bin/env python3
"""
Syncs Claude configuration files to the public reference repository.

This script copies Claude config files from their source locations to
the public jamesrappazzo-claude-code-setup repository.
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple


# Default public repo location (can be overridden via environment variable)
DEFAULT_PUBLIC_REPO = Path.home() / "code" / "jamesrappazzo-claude-code-setup"

# Files to sync: (source, destination relative to public repo)
SYNC_MANIFEST: List[Tuple[Path, str]] = [
    # Global CLAUDE.md goes to root of public repo
    (Path.home() / ".claude" / "CLAUDE.md", "CLAUDE.md"),
    # Project settings (from personal-website)
    (Path(__file__).parent.parent.parent.parent / "settings.json", ".claude/settings.json"),
]

# Directories to sync entirely
SYNC_DIRECTORIES: List[Tuple[Path, str]] = [
    # The skill itself
    (Path(__file__).parent.parent, ".claude/skills/claude-setup-blog"),
]


def get_public_repo_path() -> Path:
    """Get the public repo path from environment or default."""
    env_path = os.environ.get("CLAUDE_CONFIG_PUBLIC_REPO")
    if env_path:
        return Path(env_path)
    return DEFAULT_PUBLIC_REPO


def sync_file(source: Path, dest: Path) -> bool:
    """
    Copy a single file, creating parent directories as needed.

    Returns True if file was changed, False if unchanged.
    """
    if not source.exists():
        print(f"  Skipping (not found): {source}")
        return False

    try:
        dest.parent.mkdir(parents=True, exist_ok=True)

        # Check if file changed
        if dest.exists():
            with open(source, 'rb') as f:
                source_content = f.read()
            with open(dest, 'rb') as f:
                dest_content = f.read()
            if source_content == dest_content:
                print(f"  Unchanged: {dest.name}")
                return False

        shutil.copy2(source, dest)
        print(f"  Synced: {source.name} -> {dest}")
        return True
    except (IOError, OSError) as e:
        print(f"  ERROR syncing {source.name}: {e}")
        return False


def sync_directory(source: Path, dest: Path, dest_rel: str) -> List[str]:
    """
    Recursively sync a directory.

    Args:
        source: Source directory path
        dest: Destination directory path
        dest_rel: Relative path string for the destination (used for reporting)

    Returns list of synced file paths (relative to repo root).
    """
    synced = []

    if not source.exists():
        print(f"  Skipping (not found): {source}")
        return synced

    try:
        # Remove destination directory to ensure clean sync
        if dest.exists():
            shutil.rmtree(dest)

        # Copy entire directory
        shutil.copytree(source, dest)

        # List all files that were copied
        for root, dirs, files in os.walk(dest):
            for f in files:
                filepath = Path(root) / f
                # Calculate relative path from dest, then prepend dest_rel
                rel_to_dest = filepath.relative_to(dest)
                full_rel = f"{dest_rel}/{rel_to_dest}"
                synced.append(full_rel)
                print(f"  Synced: {full_rel}")

        return synced
    except (IOError, OSError) as e:
        print(f"  ERROR syncing directory {source}: {e}")
        return synced


def sync_to_public_repo(dry_run: bool = False) -> List[str]:
    """
    Sync all Claude config files to the public repository.

    Args:
        dry_run: If True, only print what would be synced

    Returns:
        List of files that were changed
    """
    public_repo = get_public_repo_path()
    changed_files = []

    print(f"Public repo: {public_repo}")

    if not public_repo.exists():
        print(f"ERROR: Public repo not found at {public_repo}")
        print("Set CLAUDE_CONFIG_PUBLIC_REPO environment variable or clone the repo.")
        return []

    if dry_run:
        print("\n[DRY RUN] Would sync:")
    else:
        print("\nSyncing files...")

    # Sync individual files
    for source, dest_rel in SYNC_MANIFEST:
        dest = public_repo / dest_rel
        if dry_run:
            print(f"  {source} -> {dest}")
        else:
            if sync_file(source, dest):
                changed_files.append(dest_rel)

    # Sync directories
    for source, dest_rel in SYNC_DIRECTORIES:
        dest = public_repo / dest_rel
        if dry_run:
            print(f"  {source}/ -> {dest}/")
        else:
            dir_changes = sync_directory(source, dest, dest_rel)
            changed_files.extend(dir_changes)

    return changed_files


if __name__ == "__main__":
    import sys

    dry_run = "--dry-run" in sys.argv

    changed = sync_to_public_repo(dry_run=dry_run)

    if changed and not dry_run:
        print(f"\n{len(changed)} files synced.")
    elif not dry_run:
        print("\nNo files changed.")
