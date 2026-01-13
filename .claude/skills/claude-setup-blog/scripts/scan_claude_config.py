#!/usr/bin/env python3
"""
Scans Claude Code configuration and generates structured data for blog post.

IMPORTANT: This script sanitizes output to prevent leaking sensitive information
when publishing to a public blog. See SENSITIVE_PATTERNS and SKIP_FILES.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any


# =============================================================================
# SANITIZATION CONFIG - Edit these to customize filtering
# =============================================================================

# Files to skip entirely (never include in output)
SKIP_FILES = [
    ".credentials.json",
    "credentials.json",
    ".mcp.json",
    "mcp.json",
]

# Patterns that indicate sensitive data - entries matching these are redacted
SENSITIVE_PATTERNS = [
    # Work/employer domains - ADD YOUR EMPLOYER DOMAIN HERE
    # r"example\.com",
    # Common sensitive URL patterns
    r"internal\.",
    r"corp\.",
    r"private\.",
    r"staging\.",
    r"prod\.",
    # Tokens and secrets
    r"sk-ant-",
    r"sk-[a-zA-Z0-9]{20,}",
    r"token",
    r"secret",
    r"password",
    r"credential",
    # Database URLs
    r"postgres://",
    r"postgresql://",
    r"mysql://",
    r"mongodb://",
    r"redis://",
]

# Keys to always redact from settings (even if values look safe)
REDACT_KEYS = [
    "accessToken",
    "refreshToken",
    "clientSecret",
    "apiKey",
    "password",
    "credentials",
]

# MCP servers to exclude (by name pattern)
EXCLUDE_MCP_SERVERS = [
    r"postgres",
    r"database",
    r"db-",
    r"prod",
    r"staging",
    r"internal",
    # Add work-related MCP server names here
]


def is_sensitive(value: str) -> bool:
    """Check if a string value contains sensitive patterns."""
    if not isinstance(value, str):
        return False
    for pattern in SENSITIVE_PATTERNS:
        if re.search(pattern, value, re.IGNORECASE):
            return True
    return False


def sanitize_dict(data: Dict[str, Any], depth: int = 0) -> Dict[str, Any]:
    """Recursively sanitize a dictionary, redacting sensitive values."""
    if depth > 10:  # Prevent infinite recursion
        return {"_redacted": "max depth exceeded"}

    sanitized = {}
    for key, value in data.items():
        # Always redact certain keys
        if key.lower() in [k.lower() for k in REDACT_KEYS]:
            sanitized[key] = "[REDACTED]"
        elif isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, depth + 1)
        elif isinstance(value, list):
            sanitized[key] = [
                sanitize_dict(item, depth + 1) if isinstance(item, dict)
                else "[REDACTED]" if is_sensitive(str(item))
                else item
                for item in value
            ]
        elif is_sensitive(str(value)):
            sanitized[key] = "[REDACTED]"
        else:
            sanitized[key] = value
    return sanitized


def scan_settings() -> Dict[str, Any]:
    """Scan Claude settings files (with sanitization)."""
    claude_dir = Path.home() / ".claude"
    settings = {}

    # Check for settings files
    settings_files = [
        "settings.json",
        "settings.local.json",
    ]

    for filename in settings_files:
        # Skip sensitive files entirely
        if filename in SKIP_FILES:
            continue

        filepath = claude_dir / filename
        if filepath.exists():
            try:
                with open(filepath) as f:
                    raw_settings = json.load(f)
                    # Sanitize before returning
                    settings[filename] = sanitize_dict(raw_settings)
            except Exception as e:
                settings[filename] = f"Error reading: {e}"

    return settings


def should_exclude_mcp_server(server_name: str) -> bool:
    """Check if an MCP server should be excluded from output."""
    for pattern in EXCLUDE_MCP_SERVERS:
        if re.search(pattern, server_name, re.IGNORECASE):
            return True
    return False


def scan_mcp_servers() -> Dict[str, Any]:
    """Scan for MCP server configurations (with sanitization).

    NOTE: MCP configs often contain sensitive URLs and credentials.
    This function excludes work-related servers and redacts sensitive values.
    Consider setting this to return empty if you don't want ANY MCP info published.
    """
    claude_dir = Path.home() / ".claude"

    # SAFETY: Skip MCP config entirely - it's too risky to publish
    # Uncomment the return below to completely disable MCP scanning
    # return {"_note": "MCP configuration not published for security"}

    mcp_config = {}

    # Check mcp.json (but it's in SKIP_FILES, so this is defensive)
    mcp_file = claude_dir / "mcp.json"
    if mcp_file.exists():
        try:
            with open(mcp_file) as f:
                raw_config = json.load(f)

            # Filter out sensitive servers
            if "mcpServers" in raw_config:
                filtered_servers = {}
                for name, config in raw_config.get("mcpServers", {}).items():
                    if should_exclude_mcp_server(name):
                        continue  # Skip this server entirely
                    # Sanitize the config
                    filtered_servers[name] = sanitize_dict(config) if isinstance(config, dict) else config

                if filtered_servers:
                    mcp_config["mcpServers"] = filtered_servers
                else:
                    mcp_config["_note"] = "No MCP servers configured (or all filtered for privacy)"

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
    """Scan project-specific Claude settings (with sanitization)."""
    if project_path is None:
        project_path = Path.cwd()

    settings = {}
    claude_dir = project_path / ".claude"

    if claude_dir.exists():
        # Check for settings.json (shared) and settings.local.json (local overrides)
        for filename in ["settings.json", "settings.local.json"]:
            # Skip files in the skip list
            if filename in SKIP_FILES:
                continue

            settings_file = claude_dir / filename
            if settings_file.exists():
                try:
                    with open(settings_file) as f:
                        raw_settings = json.load(f)
                        # Sanitize before returning
                        settings[filename] = sanitize_dict(raw_settings)
                except Exception as e:
                    settings[filename] = f"Error: {e}"

    return settings


def generate_config_report() -> Dict[str, Any]:
    """Generate complete configuration report (sanitized for public sharing)."""
    return {
        "_sanitization_note": "This output has been filtered. See SENSITIVE_PATTERNS in script.",
        "global_settings": scan_settings(),
        "mcp_servers": scan_mcp_servers(),
        "installed_skills": scan_skills(),
        "hooks": scan_hooks(),
        "project_settings": scan_project_settings()
    }


def print_sanitization_config():
    """Print current sanitization configuration for review."""
    print("=" * 60)
    print("SANITIZATION CONFIGURATION")
    print("=" * 60)
    print("\nFiles skipped entirely:")
    for f in SKIP_FILES:
        print(f"  - {f}")
    print("\nSensitive patterns (values matching these are redacted):")
    for p in SENSITIVE_PATTERNS:
        print(f"  - {p}")
    print("\nKeys always redacted:")
    for k in REDACT_KEYS:
        print(f"  - {k}")
    print("\nMCP servers excluded (by name pattern):")
    for p in EXCLUDE_MCP_SERVERS:
        print(f"  - {p}")
    print("=" * 60)


if __name__ == "__main__":
    import sys

    if "--show-config" in sys.argv:
        # Show what will be filtered
        print_sanitization_config()
    elif "--dry-run" in sys.argv:
        # Show config + output for review before publishing
        print_sanitization_config()
        print("\nSANITIZED OUTPUT PREVIEW:")
        print("-" * 60)
        report = generate_config_report()
        print(json.dumps(report, indent=2))
    else:
        # Normal operation - generate sanitized report
        report = generate_config_report()
        print(json.dumps(report, indent=2))
