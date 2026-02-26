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
- **Custom layout**: `layouts/index.html` — homepage with pinned posts section and writing section
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
