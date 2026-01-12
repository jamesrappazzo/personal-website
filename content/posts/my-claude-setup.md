---
title: "My Claude Code Setup"
date: 2026-01-11
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

**Last Updated:** 2026-01-11

**Browse my config files:**
- [CLAUDE.md](https://github.com/jamesrappazzo/personal-website/blob/main/.claude/CLAUDE.md) — My global instructions for Claude
- [Project settings](https://github.com/jamesrappazzo/personal-website/blob/main/.claude/settings.json) — Permissions for this repo
- [claude-setup-blog skill](https://github.com/jamesrappazzo/personal-website/tree/main/.claude/skills/claude-setup-blog) — The skill that generates this post

---

## What is Claude Code?

**Claude Code** is Anthropic's agentic coding tool that lives in your terminal. It understands your codebase, executes routine tasks, explains complex code, and handles git workflows—all through natural language. [Learn more →](https://code.claude.com/docs/en/overview)

I use it as my primary development assistant for everything from writing features to reviewing code to managing git workflows.

---

## CLAUDE.md

**What is CLAUDE.md?** A special file that Claude automatically pulls into context when starting a conversation. It's where you tell Claude about yourself, your preferences, and project-specific instructions. [Learn more →](https://docs.anthropic.com/en/docs/claude-code/memory)

**My CLAUDE.md:** [View file →](https://github.com/jamesrappazzo/personal-website/blob/main/.claude/CLAUDE.md)

Key things I tell Claude:
- I'm a TypeScript developer using React, Next.js, Tailwind, and Prisma
- My git workflow: feature branch → `/feature-dev` → rebase → squash → PR → `/code-review`
- Match existing code style, explain tradeoffs, prefer practical over over-engineered

---

## Plugins

**What are plugins?** Plugins extend Claude Code with specialized capabilities—from document editing to code review. A plugin can include slash commands, agents, skills, hooks, and MCP servers. [Learn more →](https://code.claude.com/docs/en/plugins)

I have the following plugins enabled:

| Plugin | What I Use It For |
|--------|-------------------|
| [**document-skills**](https://github.com/anthropics/skills) | Creating and editing DOCX, PDF, XLSX, PPTX files |
| [**frontend-design**](https://github.com/anthropics/claude-plugins-official) | Building production-grade UI with good design patterns |
| [**github**](https://github.com/anthropics/claude-plugins-official) | PR management, issues, and GitHub workflows |
| [**feature-dev**](https://github.com/anthropics/claude-plugins-official) | Guided feature development with codebase exploration |
| [**code-review**](https://github.com/anthropics/claude-plugins-official) | AI-powered code review on pull requests |
| [**typescript-lsp**](https://github.com/anthropics/claude-plugins-official) | Better TypeScript understanding via language server |
| [**security-guidance**](https://github.com/anthropics/claude-plugins-official) | Security best practices and vulnerability detection |
| [**commit-commands**](https://github.com/anthropics/claude-plugins-official) | Git workflow automation (`/commit`, `/commit-push-pr`) |
| [**agent-sdk-dev**](https://github.com/anthropics/claude-plugins-official) | Building Claude Agent SDK applications |
| [**stripe**](https://github.com/anthropics/claude-plugins-official) | Stripe integration utilities |

---

## Skills

**What are skills?** A skill is a markdown file that teaches Claude how to do something specific. When you ask Claude something that matches a skill's purpose, Claude automatically loads and applies it. Skills can bundle instructions, scripts, and templates. [Learn more →](https://code.claude.com/docs/en/skills)

I have one custom skill:

| Skill | What It Does |
|-------|--------------|
| [**claude-setup-blog**](https://github.com/jamesrappazzo/personal-website/tree/main/.claude/skills/claude-setup-blog) | Scans my Claude config and generates this blog post |

The skill is self-improving: each time it runs, it updates itself with new knowledge from documentation.

---

## Permissions

**What are permissions?** Claude Code uses an allow/deny/ask system to control what actions it can take. Rules are checked in order: deny rules block regardless of other rules, allow rules permit if matched, and ask rules prompt for approval. [Learn more →](https://code.claude.com/docs/en/settings)

### Global Permissions

Save this to `~/.claude/settings.json`:

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

### Project Permissions

**My project settings:** [View file →](https://github.com/jamesrappazzo/personal-website/blob/main/.claude/settings.json)

**What this enables:**
- Full git workflow (commit, push, pull, rebase)
- GitHub CLI for PRs and API access
- Hugo development server
- Python scripts for automation
- Web searches for documentation

---

## MCP Servers

**What are MCP servers?** MCP (Model Context Protocol) is an open standard for AI-tool integrations. MCP servers give Claude Code access to external tools, databases, and APIs. [Learn about MCP →](https://code.claude.com/docs/en/mcp)

I don't currently use MCP servers. [Get started with MCP →](https://modelcontextprotocol.io/)

---

## Hooks

**What are hooks?** Hooks are user-defined shell commands that execute at various points in Claude Code's lifecycle. They provide deterministic control—ensuring certain actions always happen rather than relying on the LLM to choose to run them. [Learn about hooks →](https://code.claude.com/docs/en/hooks-guide)

I don't currently use Claude hooks or git hooks with Claude Code.

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

### Step 4: Create Your CLAUDE.md

Create `~/.claude/CLAUDE.md` with your preferences. [See mine for inspiration →](https://github.com/jamesrappazzo/personal-website/blob/main/.claude/CLAUDE.md)

### Step 5: Configure Global Permissions

Create `~/.claude/settings.json`:

```bash
cat > ~/.claude/settings.json << 'EOF'
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

### Step 6: Get the claude-setup-blog Skill

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

**CLAUDE.md:** Tells Claude who I am and how I work. It's the most impactful file for personalizing Claude's behavior.

**Plugins:** I enable plugins for workflows I use regularly. Document creation, code review, and git automation save me significant time.

**Permissions:** I use an allow-list approach—explicitly permit operations I need, deny sensitive auth commands. This keeps Claude productive while maintaining security boundaries.

**Skills:** I build custom skills for repeated workflows. The claude-setup-blog skill keeps this documentation in sync automatically.

---

## Changelog

### 2026-01-11

**Added**
- CLAUDE.md section with link to my config file
- Source links for all plugins (GitHub repos)
- Links to all config files in this repo
- "Browse my config files" quick links at top

**Changed**
- Plugins and skills now use table format with source links
- Restructured for better navigation

### 2026-01-11 (earlier)

**Added**
- Beginner-friendly explanations for plugins, skills, and permissions
- Documentation links to official sources
- Global deny rules for authentication commands

### 2026-01-10

**Added**
- Initial setup documentation
- Global settings and permissions configuration
- claude-setup-blog skill for auto-generating this post

---

## Files in This Repo

| File | Description |
|------|-------------|
| [.claude/CLAUDE.md](https://github.com/jamesrappazzo/personal-website/blob/main/.claude/CLAUDE.md) | My global Claude instructions |
| [.claude/settings.json](https://github.com/jamesrappazzo/personal-website/blob/main/.claude/settings.json) | Project permissions |
| [.claude/skills/claude-setup-blog/](https://github.com/jamesrappazzo/personal-website/tree/main/.claude/skills/claude-setup-blog) | The skill that generates this post |

---

## Resources

- [Claude Code Overview](https://code.claude.com/docs/en/overview)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Plugins Documentation](https://code.claude.com/docs/en/plugins)
- [Skills Documentation](https://code.claude.com/docs/en/skills)
- [Settings & Permissions](https://code.claude.com/docs/en/settings)
- [Hooks Guide](https://code.claude.com/docs/en/hooks-guide)
- [MCP Documentation](https://code.claude.com/docs/en/mcp)
- [CLAUDE.md Guide](https://docs.anthropic.com/en/docs/claude-code/memory)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Official Plugins Repo](https://github.com/anthropics/claude-plugins-official)
- [Document Skills (xlsx, docx, pdf, pptx)](https://github.com/anthropics/skills)

---

*This post is automatically generated using my [claude-setup-blog skill](https://github.com/jamesrappazzo/personal-website/tree/main/.claude/skills/claude-setup-blog). The skill scans my configuration, researches current documentation, and regenerates this content.*
