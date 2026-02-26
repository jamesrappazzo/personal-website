---
title: "My Claude Code Setup"
date: 2026-02-26
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

**Last Updated:** 2026-02-26

**Browse my config files:**
- [CLAUDE.md](https://github.com/jamesrappazzo/personal-website/blob/main/.claude/CLAUDE.md) — My instructions for Claude
- [settings.json](https://github.com/jamesrappazzo/personal-website/blob/main/.claude/settings.json) — Permissions for this repo
- [claude-setup-blog skill](https://github.com/jamesrappazzo/personal-website/tree/main/.claude/skills/claude-setup-blog) — The skill that generates this post


## What is Claude Code?

**Claude Code** is Anthropic's agentic coding tool that lives in your terminal. It understands your codebase, executes routine tasks, explains complex code, and handles git workflows—all through natural language. [Learn more →](https://code.claude.com/docs/en/overview)

I use it as my primary development assistant for everything from writing features to reviewing code to managing git workflows.


## CLAUDE.md

**What is CLAUDE.md?** A special file that Claude automatically pulls into context when starting a conversation. It's where you tell Claude about yourself, your preferences, and project-specific instructions. Claude reads CLAUDE.md files at multiple levels — global (`~/.claude/CLAUDE.md`) for personal preferences and project-level (`.claude/CLAUDE.md`) for repo-specific context. [Learn more →](https://code.claude.com/docs/en/memory)

### Global CLAUDE.md

My global `~/.claude/CLAUDE.md` tells Claude who I am across all projects:
- I'm a TypeScript developer using React, Next.js, Tailwind, and Prisma
- My git workflow: feature branch → `/feature-dev` → rebase → squash → PR → `/code-review`
- Match existing code style, explain tradeoffs, prefer practical over over-engineered

### Project CLAUDE.md

Each repo gets its own CLAUDE.md with project-specific context. For example, [this repo's CLAUDE.md →](https://github.com/jamesrappazzo/personal-website/blob/main/.claude/CLAUDE.md) includes Hugo build commands, the site architecture, and custom skill references.


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
| [**vercel**](https://github.com/anthropics/claude-plugins-official) | Vercel deployment and project management |
| [**claude-md-management**](https://github.com/anthropics/claude-plugins-official) | Auditing and improving CLAUDE.md files |


## Skills

**What are skills?** A skill is a markdown file that teaches Claude how to do something specific. When you ask Claude something that matches a skill's purpose, Claude automatically loads and applies it. Skills can bundle instructions, scripts, and templates. [Learn more →](https://code.claude.com/docs/en/skills)

I have one custom skill:

| Skill | What It Does |
|-------|--------------|
| [**claude-setup-blog**](https://github.com/jamesrappazzo/personal-website/tree/main/.claude/skills/claude-setup-blog) | Scans my Claude config and generates this blog post |

The skill is self-improving: each time it runs, it updates itself with new knowledge from documentation.


## Permissions

**What are permissions?** Claude Code uses an allow/deny/ask system to control what actions it can take. Rules are checked in order: deny rules block regardless of other rules, allow rules permit if matched, and ask rules prompt for approval. [Learn more →](https://code.claude.com/docs/en/settings)

**A note on permission drift:** Project `settings.json` grows over time as you approve Claude's permission prompts. It's easy to approve something risky in the moment — you're focused on the task, not thinking about the permanent permission you're granting. Over time, dangerous permissions like `python:*` and `curl:*` can accumulate in your allow list. I built a [permissions audit](#permissions-audit) into my scanner to catch this.

### Global Permissions

These live in `~/.claude/settings.local.json` (not checked into repos):

```json
{
  "permissions": {
    "allow": [
      "WebSearch",
      "WebFetch(domain:code.claude.com)",
      "WebFetch(domain:docs.anthropic.com)",
      "WebFetch(domain:github.com)",
      "WebFetch(domain:www.npmjs.com)",
      "Skill(frontend-design)",
      "Skill(document-skills:skill-creator)",
      "Bash(git status:*)",
      "Bash(git log:*)",
      "Bash(git show:*)",
      "Bash(git diff:*)",
      "Bash(git fetch:*)",
      "Bash(git branch:*)",
      "Bash(git checkout:*)",
      "Bash(git switch:*)",
      "Bash(git stash:*)",
      "Bash(git restore:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(git pull:*)",
      "Bash(git rebase:*)",
      "Bash(git cherry-pick:*)",
      "Bash(gh pr view:*)",
      "Bash(gh pr list:*)",
      "Bash(gh pr create:*)",
      "Bash(gh pr close:*)",
      "Bash(gh repo view:*)",
      "Bash(gh run:*)",
      "Bash(gh workflow run:*)",
      "Bash(gh api:*)",
      "Bash(npx tsc:*)",
      "Bash(npx prisma generate:*)",
      "Bash(npx prisma db push:*)"
    ],
    "deny": [
      "Bash(gh auth:*)",
      "Bash(gh ssh-key:*)",
      "Bash(ssh-keygen:*)",
      "Bash(python:*)",
      "Bash(python3:*)",
      "Bash(curl:*)",
      "Bash(wget:*)",
      "Bash(nc:*)",
      "Bash(netcat:*)",
      "Bash(git filter-branch:*)",
      "Bash(git reset --hard:*)",
      "Bash(git push --force:*)",
      "Bash(git push -f:*)",
      "Bash(rm -rf:*)",
      "Bash(rm -r /:*)",
      "Bash(sudo:*)",
      "Bash(chmod 777:*)",
      "Bash(pkill:*)",
      "Bash(kill -9:*)",
      "Bash(killall:*)",
      "Bash(eval:*)",
      "Bash(exec:*)",
      "Bash(source:*)",
      "Bash(. :*)",
      "Bash(bash -c:*)",
      "Bash(sh -c:*)",
      "Bash(zsh -c:*)",
      "Bash(env:*)",
      "Bash(export:*)",
      "Bash(open:*)",
      "Bash(osascript:*)",
      "Bash(security:*)",
      "Bash(keychain:*)",
      "Bash(npx vercel:*)",
      "Bash(vercel:*)",
      "Bash(docker run:*)",
      "Bash(docker exec:*)",
      "Bash(docker-compose:*)",
      "Bash(kubectl:*)",
      "Bash(aws:*)",
      "Bash(gcloud:*)",
      "Bash(az:*)",
      "Bash(scp:*)",
      "Bash(rsync:*)",
      "Bash(ssh:*)",
      "Bash(base64 -d:*)",
      "Bash(xxd:*)"
    ]
  }
}
```

**Why these settings?**
- **Allow** web access to documentation domains, full git workflow, GitHub CLI for PRs, and TypeScript/Prisma tooling
- **Deny** arbitrary code execution (`python`, `curl`, `eval`, `bash -c`, `source`), authentication changes, destructive git ops (`--force`, `--hard`, `filter-branch`), process management, macOS keychain access, environment manipulation (`env`, `export`), binary decoding (`base64 -d`, `xxd`), and cloud/infra tools (`aws`, `gcloud`, `az`, `kubectl`, `docker`)

### Project Permissions

**My settings:** [View file →](https://github.com/jamesrappazzo/personal-website/blob/main/.claude/settings.json)

Project permissions in `.claude/settings.json` are checked into the repo. I keep a curated allow list and an explicit deny list:

**What this enables:**
- Hugo development server and build commands
- Standard git workflow (commit, push, pull, rebase)
- GitHub CLI for PRs and workflow management
- Web searches and documentation fetches

**What this denies:**
- Arbitrary HTTP requests (`curl`, `wget`)
- Authentication changes (`gh auth`, `gh ssh-key`)
- Destructive git operations (`filter-branch`, `reset --hard`, `push --force`)
- Git config and remote modification
- Shell execution (`eval`, `exec`, `bash -c`, `ssh`)

### Permissions Audit

My [scanner script](https://github.com/jamesrappazzo/personal-website/blob/main/.claude/skills/claude-setup-blog/scripts/scan_claude_config.py) includes a permissions audit that checks for risky patterns:

```bash
python scripts/scan_claude_config.py --audit
```

It flags issues by severity (critical/high/medium) and catches:
- Dangerous commands in allow lists (arbitrary execution, data exfiltration)
- Empty deny lists (no guardrails)
- Conflicts between project allows and global denies


## MCP Servers

**What are MCP servers?** MCP (Model Context Protocol) is an open standard for AI-tool integrations. MCP servers give Claude Code access to external tools, databases, and APIs. [Learn about MCP →](https://code.claude.com/docs/en/mcp)

I don't currently use MCP servers. [Get started with MCP →](https://modelcontextprotocol.io/)


## Hooks

**What are hooks?** Hooks are user-defined shell commands that execute at various points in Claude Code's lifecycle. They provide deterministic control—ensuring certain actions always happen rather than relying on the LLM to choose to run them. [Learn about hooks →](https://code.claude.com/docs/en/hooks-guide)

I don't currently use Claude hooks or git hooks with Claude Code.


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
    "stripe@claude-plugins-official": true,
    "vercel@claude-plugins-official": true,
    "claude-md-management@claude-plugins-official": true
  }
}
```

### Step 4: Create Your CLAUDE.md

Create a global `~/.claude/CLAUDE.md` with your personal preferences (tech stack, workflow, communication style). Then use `/init` inside any project to generate a project-specific CLAUDE.md with build commands and architecture context. [Learn more →](https://code.claude.com/docs/en/memory)

### Step 5: Configure Global Permissions

Create `~/.claude/settings.local.json` with your personal security boundaries. Here's a minimal starting point:

```bash
cat > ~/.claude/settings.local.json << 'EOF'
{
  "permissions": {
    "allow": [
      "WebSearch",
      "WebFetch(domain:code.claude.com)",
      "WebFetch(domain:docs.anthropic.com)",
      "Bash(git status:*)",
      "Bash(git log:*)",
      "Bash(git diff:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(git pull:*)",
      "Bash(gh pr list:*)",
      "Bash(gh pr create:*)",
      "Bash(gh pr view:*)"
    ],
    "deny": [
      "Bash(gh auth:*)",
      "Bash(gh ssh-key:*)",
      "Bash(ssh-keygen:*)",
      "Bash(curl:*)",
      "Bash(python:*)",
      "Bash(eval:*)",
      "Bash(bash -c:*)",
      "Bash(sudo:*)",
      "Bash(rm -rf:*)",
      "Bash(git push --force:*)",
      "Bash(git reset --hard:*)"
    ]
  }
}
EOF
```

Add more allows as you need them—Claude will prompt you. Run `python scripts/scan_claude_config.py --audit` periodically to catch permission drift.

### Step 6: Get the claude-setup-blog Skill

Clone my website repo to get the custom skill:

```bash
git clone https://github.com/jamesrappazzo/personal-website.git
cd personal-website
# The skill is at .claude/skills/claude-setup-blog/
```


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


## Why This Setup?

**CLAUDE.md:** Tells Claude who I am and how I work. It's the most impactful file for personalizing Claude's behavior.

**Plugins:** I enable plugins for workflows I use regularly. Document creation, code review, and git automation save me significant time.

**Permissions:** I use layered allow/deny lists—globally deny dangerous commands (arbitrary execution, auth changes, destructive git ops), then allow specific safe operations at the project level. I audit regularly because permissions drift over time as you approve prompts.

**Skills:** I build custom skills for repeated workflows. The claude-setup-blog skill keeps this documentation in sync automatically.


## Changelog

### 2026-02-26

**Added**
- claude-md-management plugin for auditing and improving CLAUDE.md files
- Additional global deny rules: script sourcing (`source`, `.`), environment manipulation (`env`, `export`), macOS keychain access (`security`, `keychain`), Vercel CLI (`npx vercel`, `vercel`), Azure CLI (`az`), Docker Compose, and binary decoding (`base64 -d`, `xxd`)

**Changed**
- Updated global deny list to match current configuration (16 new entries)

### 2026-02-10

**Added**
- Vercel plugin for deployment management
- Permissions audit tool (`--audit` flag in scanner script)
- Full global allow/deny permissions config (previously only showed a minimal subset)
- "Permission drift" explanation and audit section

**Changed**
- Cleaned up project `settings.json`: removed dangerous allows (`python`, `curl`, `gh auth`, `git filter-branch`, `git reset`), added explicit deny list
- Replication guide now uses `settings.local.json` (personal permissions) instead of `settings.json` (shared plugins)
- Updated global permissions step with a practical starter config and audit tip

**Fixed**
- Project permissions previously had an empty deny list with no guardrails

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


## Config Files

| File | Description |
|------|-------------|
| [CLAUDE.md](https://github.com/jamesrappazzo/personal-website/blob/main/.claude/CLAUDE.md) | Project-level Claude instructions (Hugo commands, site architecture) |
| [.claude/settings.json](https://github.com/jamesrappazzo/personal-website/blob/main/.claude/settings.json) | Project permissions (allow/deny) |
| [.claude/skills/claude-setup-blog/](https://github.com/jamesrappazzo/personal-website/tree/main/.claude/skills/claude-setup-blog) | The skill that generates this post |


## Resources

- [My Website Repo](https://github.com/jamesrappazzo/personal-website) — Source for this site, includes all my Claude config
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

*This post is automatically generated using my [claude-setup-blog skill](https://github.com/jamesrappazzo/personal-website/tree/main/.claude/skills/claude-setup-blog). The skill scans my configuration and regenerates this content.*
