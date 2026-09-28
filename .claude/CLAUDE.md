# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About Me

I'm James, a web developer working primarily with TypeScript.

## Project Overview

Personal website and blog built with Hugo and the PaperMod theme, deployed to GitHub Pages at jamesrappazzo.com.

## Commands

```bash
hugo server              # Local dev server with hot reload (localhost:1313)
hugo server -D           # Include draft posts
hugo --minify            # Production build to public/
hugo version             # Check Hugo version (requires 0.146.0+)
```

The scanner script for the claude-setup-blog skill:
```bash
cd .claude/skills/claude-setup-blog
python3 scripts/scan_claude_config.py          # Full config scan (JSON)
python3 scripts/scan_claude_config.py --audit  # Permissions security audit
```

## Architecture

- **Hugo config**: `hugo.toml` — site settings, menu, social icons, PaperMod params
- **Theme**: `themes/PaperMod/` (git submodule) — do not edit directly
- **Content**: `content/posts/` for blog posts, `content/about.md` for about page
- **Custom layout**: `layouts/index.html` — homepage: intro (heading from `heading` and text from the body of `content/_index.md`, whose `title` stays the site title so `<title>` and RSS are unchanged), pinned posts section and writing section
- **Content from Obsidian**: `obsidian-hugo.toml` maps vault notes to content files (posts in `content/posts/<slug>/index.md`, Home → `content/_index.md`, About → `content/about.md`); the obsidian plugin's hugo-publish skill writes them. Edit those in the vault, not here.
- **Custom CSS**: `assets/css/extended/custom.css` — industrial minimal theme (rust/steel palette, DM Sans + JetBrains Mono)
- **Deploy**: `.github/workflows/hugo.yml` — builds on push to main, deploys to GitHub Pages
- **Domain**: `static/CNAME` — custom domain config

### Content Frontmatter

Posts support these custom fields:
- `pinned: true` — shows in the pinned section on homepage
- `ShowToc: true` / `TocOpen: true` — table of contents
- `draft: true` — excluded from production builds

### Custom Skill: claude-setup-blog

Located at `.claude/skills/claude-setup-blog/`. Scans Claude Code configuration and generates `content/posts/my-claude-setup.md`. The scanner sanitizes sensitive data before publishing. Invoke with `/claude-setup-blog`.

## Git Workflow

For each distinct task:

1. **Setup**: Create a new feature branch
2. **Development**: Use `/feature-dev` for new features (and `/frontend-design` for UI work when relevant)
3. **Commit & PR**: Rebase on main, squash commits, commit with conventional commit format, push, and open PR
4. **Review**: Run `/code-review`, address feedback, squash again if needed, then push

## Preferences

### Code Style
- Match the existing style in whatever project I'm working on
- Follow established patterns and conventions already in the codebase

### Communication
- When uncertain about an approach, explain the tradeoffs between options rather than just picking one
- Keep responses balanced—explain key decisions but don't over-explain obvious things

### Development Approach
- Prefer practical solutions over over-engineered abstractions

## Shepherd Contract

- **Tracker** — GitHub Issues on this repo (optional: most changes are asked for in chat and go straight to a PR)
- **Issue id** — `#<N>`
- **Read a ticket** — `gh issue view <N> --json state,title`
- **Branch** — `<type>/<short-slug>` (post branches from the hugo-publish skill: `post/<slug>`)
- **Commit** — conventional commits
- **PR title** — `<type>: <summary>`
- **PR closes** — `Closes #<N>` in the PR body when there is an issue
- **Close the ticket** — automatic, from that line
- **Merge** — `gh pr merge <PR> --squash --delete-branch`, run by the owner, never an agent
- **Worktree create** — `git worktree add ../personal-website-<slug> -b <branch> origin/main && git -C ../personal-website-<slug> submodule update --init`
- **Worktree remove** — `git worktree remove ../personal-website-<slug>`
- **Gates** — `hugo --minify -d <tmp dir>` with Hugo matching `HUGO_VERSION` in `.github/workflows/hugo.yml`: no `ERROR` lines
- **CI status** — none on PRs; CI builds and deploys on push to `main`
- **Dev server** — `hugo server -p <port> --bind 127.0.0.1`
- **Evidence** — `.evidence/` (outside `content/` and `static/`, so Hugo never publishes it)
- **Human sign-off** — every merge (merging to `main` deploys the live site)
