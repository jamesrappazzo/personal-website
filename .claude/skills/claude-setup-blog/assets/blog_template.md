---
title: "My Claude Code Setup"
date: {DATE}
draft: false
tags: ["claude", "AI", "development", "tooling"]
categories: ["Development"]
description: "My Claude Code configuration, plugins, and workflows"
ShowToc: true
TocOpen: true
pinned: true
---

## Overview

My current Claude Code configuration—automatically kept in sync by a custom skill.

**Last Updated:** {DATE}

**Browse my config files:** [jamesrappazzo/jamesrappazzo-claude-code-setup](https://github.com/jamesrappazzo/jamesrappazzo-claude-code-setup)
- [CLAUDE.md](https://github.com/jamesrappazzo/jamesrappazzo-claude-code-setup/blob/main/CLAUDE.md) — My global instructions for Claude
- [.claude/settings.json](https://github.com/jamesrappazzo/jamesrappazzo-claude-code-setup/blob/main/.claude/settings.json) — Permissions configuration
- [claude-setup-blog skill](https://github.com/jamesrappazzo/jamesrappazzo-claude-code-setup/tree/main/.claude/skills/claude-setup-blog) — The skill that generates this post

## What is Claude Code?

Claude Code is Anthropic's official CLI tool that brings Claude AI into your terminal and development workflow. It provides an interactive agent that can read, write, and execute code with full context of your project. [Learn more →](https://code.claude.com/docs/en/overview)

## My Configuration

### Global Settings

{GLOBAL_SETTINGS}

### Enabled Plugins

{ENABLED_PLUGINS}

### MCP Servers

{MCP_SERVERS}

### Installed Skills

{INSTALLED_SKILLS}

## Project-Specific Settings

{PROJECT_SETTINGS}

## Hooks & Automations

{HOOKS}

## How to Use This Setup

### Installation

1. Install Claude Code:
```bash
npm install -g @anthropic-ai/claude-code
```

2. Authenticate:
```bash
claude auth
```

### Replicating My Configuration

{SETUP_INSTRUCTIONS}

## Workflows & Tips

{WORKFLOWS}

## Why This Setup?

{RATIONALE}

## Files in This Setup

| File | Description |
|------|-------------|
| [CLAUDE.md](https://github.com/jamesrappazzo/jamesrappazzo-claude-code-setup/blob/main/CLAUDE.md) | My global Claude instructions |
| [.claude/settings.json](https://github.com/jamesrappazzo/jamesrappazzo-claude-code-setup/blob/main/.claude/settings.json) | Permissions configuration |
| [.claude/skills/claude-setup-blog/](https://github.com/jamesrappazzo/jamesrappazzo-claude-code-setup/tree/main/.claude/skills/claude-setup-blog) | The skill that generates this post |

## Resources

- [Claude Code Documentation](https://code.claude.com/docs/en/overview)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [CLAUDE.md Guide](https://docs.anthropic.com/en/docs/claude-code/memory)
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io/)
- [My Config Files Repo](https://github.com/jamesrappazzo/jamesrappazzo-claude-code-setup)

---

*This post is automatically generated using my [claude-setup-blog skill](https://github.com/jamesrappazzo/jamesrappazzo-claude-code-setup/tree/main/.claude/skills/claude-setup-blog). The skill scans my configuration, syncs it to the public repo, and regenerates this content.*
