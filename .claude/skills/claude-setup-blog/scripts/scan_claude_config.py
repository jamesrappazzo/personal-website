#!/usr/bin/env python3
"""
Scans Claude Code configuration and generates structured data for blog post.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any


def scan_settings() -> Dict[str, Any]:
    """Scan Claude settings files."""
    claude_dir = Path.home() / ".claude"
    settings = {}

    # Check for settings files
    settings_files = [
        "settings.json",
        "settings.local.json",
    ]

    for filename in settings_files:
        filepath = claude_dir / filename
        if filepath.exists():
            try:
                with open(filepath) as f:
                    settings[filename] = json.load(f)
            except Exception as e:
                settings[filename] = f"Error reading: {e}"

    return settings


def scan_mcp_servers() -> Dict[str, Any]:
    """Scan for MCP server configurations."""
    claude_dir = Path.home() / ".claude"
    mcp_config = {}

    # Check mcp.json
    mcp_file = claude_dir / "mcp.json"
    if mcp_file.exists():
        try:
            with open(mcp_file) as f:
                mcp_config = json.load(f)
        except Exception as e:
            mcp_config = {"error": str(e)}

    return mcp_config


def scan_skills() -> List[str]:
    """Scan for installed skills."""
    claude_dir = Path.home() / ".claude"
    skills_dir = claude_dir / "skills"

    if not skills_dir.exists():
        return []

    skills = []
    for item in skills_dir.iterdir():
        if item.is_dir() and (item / "SKILL.md").exists():
            skills.append(item.name)
        elif item.suffix == ".skill":
            skills.append(item.stem)

    return sorted(skills)


def scan_hooks() -> Dict[str, List[str]]:
    """Scan for Claude hooks and git hooks."""
    hooks = {
        "claude_hooks": [],
        "git_hooks": []
    }

    # Check Claude hooks
    claude_dir = Path.home() / ".claude"
    hooks_dir = claude_dir / "hooks"
    if hooks_dir.exists():
        hooks["claude_hooks"] = [f.name for f in hooks_dir.iterdir() if f.is_file()]

    # Check git hooks in current repo
    git_hooks_dir = Path.cwd() / ".git" / "hooks"
    if git_hooks_dir.exists():
        # Filter out .sample files
        hooks["git_hooks"] = [
            f.name for f in git_hooks_dir.iterdir()
            if f.is_file() and not f.name.endswith(".sample")
        ]

    return hooks


def scan_project_settings(project_path: Path = None) -> Dict[str, Any]:
    """Scan project-specific Claude settings."""
    if project_path is None:
        project_path = Path.cwd()

    settings = {}
    claude_dir = project_path / ".claude"

    if claude_dir.exists():
        settings_file = claude_dir / "settings.local.json"
        if settings_file.exists():
            try:
                with open(settings_file) as f:
                    settings["project_settings"] = json.load(f)
            except Exception as e:
                settings["project_settings"] = f"Error: {e}"

    return settings


def generate_config_report() -> Dict[str, Any]:
    """Generate complete configuration report."""
    return {
        "global_settings": scan_settings(),
        "mcp_servers": scan_mcp_servers(),
        "installed_skills": scan_skills(),
        "hooks": scan_hooks(),
        "project_settings": scan_project_settings()
    }


if __name__ == "__main__":
    # Generate report and print as JSON
    report = generate_config_report()
    print(json.dumps(report, indent=2))
