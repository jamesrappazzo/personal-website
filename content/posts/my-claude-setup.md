---
title: "My Claude Code Setup"
date: 2026-01-11
draft: false
tags: ["claude", "ai", "development", "tooling"]
categories: ["Development"]
description: "A living document of my Claude Code configuration, plugins, and workflows"
---

## Overview

This is a living document that captures my current Claude Code setup. It's automatically updated to reflect my evolving configuration as I discover new workflows and tools.

**Last Updated:** 2026-01-11

## What is Claude Code?

Claude Code is Anthropic's official CLI tool that brings Claude AI into your terminal and development workflow. It provides an interactive agent that can read, write, and execute code with full context of your project.

## My Configuration

### Global Settings

**Model:** `sonnet` (Claude Sonnet 4.5)

I use Sonnet as my default model for the best balance of speed, capability, and cost-effectiveness for day-to-day development tasks.

**Global Permissions:**
```json
{
  "permissions": {
    "allow": [
      "WebFetch(domain:code.claude.com)"
    ],
    "deny": [],
    "ask": []
  }
}
```

### Enabled Plugins

I have the following official Claude plugins enabled:

- **document-skills** - Comprehensive document creation and editing (DOCX, PDF, XLSX, PPTX, etc.)
- **frontend-design** - Build beautiful, production-grade frontend interfaces
- **github** - GitHub integration for PR management, issues, and workflows
- **feature-dev** - Guided feature development with codebase understanding
- **code-review** - AI-powered code review for pull requests
- **typescript-lsp** - TypeScript language server integration for better code understanding
- **security-guidance** - Security best practices and vulnerability detection
- **commit-commands** - Git workflow automation (commit, push, PR creation)
- **agent-sdk-dev** - Tools for building Claude Agent SDK applications
- **stripe** - Stripe integration and payment processing utilities

### MCP Servers

**Status:** No MCP servers currently configured globally.

I'm exploring MCP (Model Context Protocol) servers to extend Claude's capabilities. MCP allows Claude to integrate with external services and APIs. Learn more at [modelcontextprotocol.io](https://modelcontextprotocol.io/).

### Installed Skills

I have the following custom skills installed:

- **claude-setup-blog** - Automatically scans Claude Code configuration and generates/updates this blog post

This skill demonstrates the power of custom skills for automating documentation and workflows.

## Project-Specific Settings

For my personal website project, I have additional permissions configured:

```json
{
  "permissions": {
    "allow": [
      "Bash(cat:*)",
      "Bash(tree:*)",
      "Bash(find:*)",
      "Bash(du:*)",
      "Bash(gh repo view:*)",
      "Bash(claude mcp list:*)",
      "Skill(document-skills:skill-creator)",
      "Bash(python:*)",
      "Bash(python3:*)",
      "Bash(claude skill install:*)",
      "Bash(git checkout:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(git restore:*)",
      "Bash(git log:*)",
      "Bash(git check-ignore:*)",
      "Bash(gh pr create:*)",
      "Bash(gh api:*)",
      "Bash(hugo:*)",
      "Bash(hugo server:*)",
      "Bash(hugo version:*)",
      "Bash(pkill hugo:*)",
      "Bash(curl:*)",
      "Bash(ls:*)",
      "Bash(awk:*)",
      "Bash(grep:*)",
      "Skill(frontend-design)",
      "WebFetch(domain:github.com)"
    ],
    "deny": [],
    "ask": []
  }
}
```

These permissions allow Claude to:
- **File exploration** - Read files, list directories, explore project structure
- **Git workflow** - Full git operations including checkout, add, commit, push, restore, and log
- **GitHub integration** - Create PRs, interact with GitHub API, view repo information
- **Hugo development** - Run Hugo dev server, build site, manage Hugo processes
- **Custom skills** - Create and install skills, use frontend-design for UI work
- **Automation** - Run Python scripts, curl requests, and shell utilities

## Hooks & Automations

**Claude Hooks:** None configured yet

**Git Hooks:** None configured yet

I plan to add hooks for automated workflows like:
- Pre-commit code formatting and linting
- Automated changelog generation
- Build validation before commits

## How to Use This Setup

### Installation

1. Install Claude Code:
```bash
npm install -g @anthropic-ai/claude-code
```

2. Authenticate with your Anthropic API key:
```bash
claude auth
```

3. Verify installation:
```bash
claude --version
```

### Replicating My Configuration

**Step 1: Configure Global Settings**

Create `~/.claude/settings.json`:
```bash
mkdir -p ~/.claude
cat > ~/.claude/settings.json << 'EOF'
{
  "model": "sonnet",
  "enabledPlugins": {
    "document-skills@anthropic-agent-skills": true,
    "frontend-design@claude-plugins-official": true,
    "github@claude-plugins-official": true,
    "feature-dev@claude-plugins-official": true,
    "code-review@claude-plugins-official": true,
    "typescript-lsp@claude-plugins-official": true,
    "security-guidance@claude-plugins-official": true,
    "commit-commands@claude-plugins-official": true,
    "agent-sdk-dev@claude-plugins-official": true,
    "stripe@claude-plugins-official": true
  }
}
EOF
```

**Step 2: Configure Permissions**

Create `~/.claude/settings.local.json`:
```bash
cat > ~/.claude/settings.local.json << 'EOF'
{
  "permissions": {
    "allow": [
      "WebFetch(domain:code.claude.com)"
    ],
    "deny": [],
    "ask": []
  }
}
EOF
```

**Step 3: Project-Specific Setup**

In your project directory, create `.claude/settings.local.json`:
```bash
mkdir -p .claude
cat > .claude/settings.local.json << 'EOF'
{
  "permissions": {
    "allow": [
      "Bash(cat:*)",
      "Bash(tree:*)",
      "Bash(find:*)",
      "Bash(du:*)",
      "Bash(gh repo view:*)",
      "Bash(claude mcp list:*)",
      "Bash(python:*)",
      "Bash(python3:*)",
      "Bash(git checkout:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(git restore:*)",
      "Bash(git log:*)",
      "Bash(gh pr create:*)",
      "Bash(gh api:*)",
      "Bash(hugo:*)",
      "Bash(hugo server:*)",
      "WebFetch(domain:github.com)"
    ],
    "deny": [],
    "ask": []
  }
}
EOF
```

**Step 4: Install Custom Skills**

If you're using my website repo, the `claude-setup-blog` skill is already included in `.claude/skills/`. To use it:

```bash
# The skill is already in the repo at .claude/skills/claude-setup-blog/
# You can invoke it by asking Claude to update your setup blog post
```

To install it globally from the packaged version:
```bash
cp .claude/skills/claude-setup-blog.skill ~/.claude/skills/
```

## Workflows & Tips

### Git Workflow
- Use `/commit` to automatically stage changes and create semantic commits with proper formatting
- Run `/commit-push-pr` to commit, push, and open a PR in one command
- Claude co-authors all commits: `Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>`

### Code Review
- Run `/code-review <PR-number>` to get AI-powered code reviews
- Claude analyzes for bugs, security issues, and code quality
- Uses confidence-based filtering to report only high-priority issues

### Document Creation
- Ask Claude to create/edit DOCX, PDF, XLSX, PPTX files directly
- Supports tracked changes, comments, and formatting preservation
- Great for technical documentation and reports

### Feature Development
- Use `/feature-dev` for guided feature implementation
- Claude explores codebase patterns and provides architecture blueprints
- Helps maintain consistency with existing code conventions

### Building Skills
- Use `/skill-creator` to build custom skills for repeated workflows
- Skills bundle scripts, references, and assets for efficiency
- Great for domain-specific knowledge and automation

## Why This Setup?

### Model Choice: Sonnet
I use Sonnet (Claude Sonnet 4.5) as my default model because:
- Best balance of speed and capability for development
- Handles complex codebases efficiently
- More cost-effective than Opus for routine tasks
- Switch to Opus with `/model opus` when I need maximum reasoning power

### Plugin Selection
My plugin choices reflect my development workflow:
- **Document tools** - Essential for creating technical documentation and specs
- **Git automation** - Streamlines the commit/PR process significantly
- **Code review** - Catches issues I might miss in my own code
- **Feature development** - Helps maintain architecture consistency
- **Security guidance** - Proactive security is critical

### Permission Philosophy
I use an "allow-list" approach:
- Explicitly allow specific operations I use regularly
- Keeps security tight while enabling productivity
- Project-specific permissions for different security contexts

### Custom Skills Philosophy
I build custom skills for:
- **Repeated workflows** - Automate processes I do frequently
- **Documentation** - Keep documentation in sync with reality
- **Domain knowledge** - Encode specialized knowledge for reuse
- **Open source sharing** - Enable others to use my workflows

## Changelog

### 2026-01-11 ([PR #3](https://github.com/jamesrappazzo/personal-website/pull/3))

**Added**
- Git workflow permissions (checkout, add, commit, push, restore, log)
- GitHub API permissions (gh pr create, gh api)
- Hugo development commands (server, build, version, pkill)
- frontend-design skill permission
- WebFetch for github.com domain

### 2026-01-10 ([PR #1](https://github.com/jamesrappazzo/personal-website/pull/1))

**Added**
- Initial setup documentation
- Global settings and permissions configuration
- Enabled plugins list with descriptions
- Project-specific permissions for personal-website
- Replication instructions and workflows
- claude-setup-blog skill for auto-generating this post

## Resources

- [Claude Code Documentation](https://code.claude.com/docs)
- [Claude API Documentation](https://docs.anthropic.com/)
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io/)
- [My Website Repository](https://github.com/jamesrappazzo/personal-website)
- [Claude Setup Blog Skill Source](.claude/skills/claude-setup-blog/)

---

*This post is automatically generated and updated using my custom `claude-setup-blog` skill. The skill scans my configuration and regenerates this content to keep it current. View the skill source in this repo at `.claude/skills/claude-setup-blog/`.*
