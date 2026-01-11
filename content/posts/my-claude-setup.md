---
title: "My Claude Code Setup"
date: 2026-01-11
draft: false
tags: ["claude", "ai", "development", "tooling"]
categories: ["Development"]
description: "A living document of my Claude Code configuration, plugins, and workflows"
ShowToc: true
TocOpen: true
---

## Overview

This is a living document that captures my current Claude Code setup. It's automatically updated to reflect my evolving configuration as I discover new workflows and tools.

**Last Updated:** 2026-01-11

## What is Claude Code?

**Claude Code** is Anthropic's agentic coding tool that lives in your terminal. It understands your codebase, executes routine tasks, explains complex code, and handles git workflows—all through natural language. [Learn more →](https://docs.anthropic.com/en/docs/claude-code/overview)

I use it as my primary development assistant for everything from writing features to reviewing code to managing git workflows.

---

## Plugins

**What are plugins?** Plugins extend Claude Code with specialized capabilities—from document editing to code review. Think of them as apps for Claude that add new skills and slash commands. [Learn more →](https://code.claude.com/docs/en/plugins)

I have the following plugins enabled:

| Plugin | What I Use It For |
|--------|-------------------|
| **document-skills** | Creating and editing DOCX, PDF, XLSX, PPTX files directly |
| **frontend-design** | Building production-grade UI with good design patterns |
| **github** | PR management, issues, and GitHub workflows |
| **feature-dev** | Guided feature development with codebase exploration |
| **code-review** | AI-powered code review on pull requests |
| **typescript-lsp** | Better TypeScript understanding via language server |
| **security-guidance** | Security best practices and vulnerability detection |
| **commit-commands** | Git workflow automation (`/commit`, `/commit-push-pr`) |
| **agent-sdk-dev** | Building Claude Agent SDK applications |
| **stripe** | Stripe integration utilities |

---

## Skills

**What are skills?** Skills are reusable prompt packages that Claude loads automatically when relevant. Unlike slash commands (which you invoke explicitly), skills are triggered by Claude based on your request. They can bundle instructions, scripts, and templates. [Learn more →](https://code.claude.com/docs/en/skills)

I have one custom skill:

- **claude-setup-blog** — Automatically scans my Claude configuration and generates this blog post. It's self-improving: each time it runs, it updates itself with new knowledge.

The skill lives in this repo at `.claude/skills/claude-setup-blog/` so anyone can use it.

---

## Permissions

**What are permissions?** Claude Code uses an allow/deny/ask system to control what actions it can take. This keeps you in control of what Claude can do on your machine. [Learn more →](https://code.claude.com/docs/en/iam)

### Global Permissions

Save this to `~/.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "WebFetch(domain:code.claude.com)"
    ],
    "deny": [
      "Bash(gh auth:*)",
      "Bash(gh ssh-key:*)",
      "Bash(ssh-keygen:*)"
    ],
    "ask": []
  }
}
```

**Why these settings?**
- **Allow** web fetches to Claude docs for reference
- **Deny** authentication commands—I don't want Claude changing my GitHub credentials

### Project Permissions (this website)

Save this to `.claude/settings.local.json` in your project:

```json
{
  "permissions": {
    "allow": [
      "Bash(cat:*)",
      "Bash(tree:*)",
      "Bash(find:*)",
      "Bash(du:*)",
      "Bash(ls:*)",
      "Bash(grep:*)",
      "Bash(awk:*)",
      "Bash(gh repo view:*)",
      "Bash(gh pr create:*)",
      "Bash(gh api:*)",
      "Bash(gh run:*)",
      "Bash(git checkout:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(git pull:*)",
      "Bash(git fetch:*)",
      "Bash(git rebase:*)",
      "Bash(git restore:*)",
      "Bash(git log:*)",
      "Bash(git filter-branch:*)",
      "Bash(git remote set-url:*)",
      "Bash(python:*)",
      "Bash(python3:*)",
      "Bash(curl:*)",
      "Bash(hugo:*)",
      "Bash(hugo server:*)",
      "Bash(hugo version:*)",
      "Bash(pkill hugo:*)",
      "Bash(pgrep:*)",
      "Skill(frontend-design)",
      "Skill(document-skills:skill-creator)",
      "WebFetch(domain:github.com)",
      "WebSearch"
    ],
    "deny": [],
    "ask": []
  }
}
```

**What this enables:**
- Full git workflow (commit, push, pull, rebase)
- GitHub CLI for PRs and API access
- Hugo development server
- Python scripts for automation
- Web searches for documentation

---

## MCP Servers

I don't currently use MCP (Model Context Protocol) servers. [Learn about MCP →](https://modelcontextprotocol.io/)

---

## Hooks

I don't currently use Claude hooks or git hooks with Claude Code. [Learn about hooks →](https://docs.anthropic.com/en/docs/claude-code/hooks)

---

## How to Replicate My Setup

### Step 1: Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

Verify:
```bash
claude --version
```

### Step 2: Authenticate

```bash
claude auth
```

### Step 3: Add Plugin Marketplace

```bash
/plugin marketplace add anthropics/claude-plugins-official
```

Then enable plugins via `/plugin` menu, or add to `~/.claude/settings.json`:

```json
{
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
```

### Step 4: Configure Global Permissions

Create `~/.claude/settings.local.json`:

```bash
cat > ~/.claude/settings.local.json << 'EOF'
{
  "permissions": {
    "allow": [
      "WebFetch(domain:code.claude.com)"
    ],
    "deny": [
      "Bash(gh auth:*)",
      "Bash(gh ssh-key:*)",
      "Bash(ssh-keygen:*)"
    ],
    "ask": []
  }
}
EOF
```

Verify:
```bash
cat ~/.claude/settings.local.json
```

### Step 5: Get the claude-setup-blog Skill

Clone this repo to get my custom skill:

```bash
git clone https://github.com/jamesrappazzo/personal-website.git
cd personal-website
# The skill is at .claude/skills/claude-setup-blog/
```

---

## Workflows I Use Daily

### Git Commits
```
/commit
```
Stages changes and creates a semantic commit with proper formatting. Claude co-authors: `Co-Authored-By: Claude <noreply@anthropic.com>`

### Code Review
```
/code-review 123
```
Reviews PR #123 for bugs, security issues, and code quality. Uses confidence scoring to surface only high-priority issues.

### Feature Development
```
/feature-dev
```
Guided feature implementation—Claude explores the codebase, understands patterns, and provides architecture blueprints.

### Commit + PR in One Step
```
/commit-push-pr
```
Commits, pushes, and opens a PR in one command.

---

## Why This Setup?

**Plugins:** I enable plugins for workflows I use regularly. Document creation, code review, and git automation save me significant time.

**Permissions:** I use an allow-list approach—explicitly permit operations I need, deny sensitive auth commands. This keeps Claude productive while maintaining security boundaries.

**Skills:** I build custom skills for repeated workflows. The claude-setup-blog skill keeps this documentation in sync automatically.

---

## Changelog

### 2026-01-11 ([PR #5](https://github.com/jamesrappazzo/personal-website/pull/5))

**Added**
- Beginner-friendly explanations for plugins, skills, and permissions
- Documentation links to official sources
- Table format for plugin list
- Updated project permissions (git rebase, filter-branch, WebSearch)
- Global deny rules for authentication commands

**Changed**
- Restructured for better readability and copy-friendliness
- Simplified "How to Replicate" section with verification steps

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

---

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code/overview)
- [Claude Code Plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Claude Code Permissions](https://code.claude.com/docs/en/iam)
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io/)
- [This Website's Repository](https://github.com/jamesrappazzo/personal-website)

---

*This post is automatically generated using my [claude-setup-blog skill](.claude/skills/claude-setup-blog/). The skill scans my configuration, researches current documentation, and regenerates this content.*
