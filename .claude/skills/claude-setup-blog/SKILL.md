---
name: claude-setup-blog
description: Automatically scan Claude Code configuration (settings, MCP servers, skills, hooks) and generate or update a blog post documenting the setup with installation instructions for others. Use when the user wants to document their Claude setup, update their setup documentation, or create a blog post about their Claude Code configuration. Triggered by requests like "update my Claude setup blog post", "document my Claude configuration", or "generate my setup documentation".
---

# Claude Setup Blog Generator

Automatically scans your Claude Code configuration and generates/updates a blog post documenting your setup for others to learn from and replicate.

## Overview

This skill helps you maintain an evergreen blog post about your Claude Code setup by:

1. Scanning your Claude configuration files (settings, MCP servers, skills, hooks)
2. Auditing permissions for security vulnerabilities
3. Syncing config files to the public reference repository
4. Generating or updating a blog post in your Hugo website
5. Creating pull requests in both repositories

The blog post includes:
- Your configuration settings
- Enabled plugins and skills
- MCP server configurations
- Hooks and automations
- Permissions security audit results
- Instructions for others to replicate your setup
- A changelog tracking all updates with PR links

## Repository Configuration

Everything lives in the **personal-website** repository (public):
- Blog post: `content/posts/my-claude-setup.md`
- Config files: `.claude/settings.json`, `.claude/CLAUDE.md`
- This skill: `.claude/skills/claude-setup-blog/`

All links in the blog post point directly to files in this repo.

## Workflow

### Step 0: Research Latest Documentation

Before generating content, use **WebSearch** to find the latest official guidance for each Claude Code feature being documented:

**Required searches:**
- "Claude Code documentation 2026" → Get latest official docs
- "Claude Code plugins guide" → Current plugin system docs
- "Claude Code MCP servers setup" → MCP configuration guide
- "Claude Code skills tutorial" → Skills documentation
- "Claude Code hooks configuration" → Hooks guide
- "Claude Code permissions settings" → Permissions reference

**For each feature mentioned, find and include:**
- Official documentation URL
- Current best practices
- Any recent changes or deprecations

Store the URLs to include as reference links in the blog post.

### Step 1: Scan Configuration

Run the configuration scanner to collect data:

```bash
python scripts/scan_claude_config.py
```

This generates a JSON report containing:
- Global settings from `~/.claude/settings.json` and `settings.local.json`
- MCP server configurations
- Installed skills list
- Claude hooks and git hooks
- Project-specific settings from `.claude/settings.local.json`

### Step 1b: Audit Permissions

Run the permissions audit to check for security issues:

```bash
python scripts/scan_claude_config.py --audit
```

This checks all permission sources (global and project settings) for:
- **Risky allow rules** flagged by severity (critical/high/medium)
- **Empty deny lists** in project settings (no guardrails)
- **Conflicts** where project allow rules contradict global deny rules

The audit results are also included in the full scan report under the `permissions_audit` key.

**If critical or high findings exist:**
1. Flag them to the user before generating the blog post
2. Recommend fixes (remove dangerous allows, add deny rules)
3. If the user approves fixes, update the settings files
4. Re-run the audit to confirm the fixes worked

**Common risky patterns detected:**

| Severity | Pattern | Risk |
|----------|---------|------|
| Critical | `Bash(python:*)` | Arbitrary code execution |
| Critical | `Bash(curl:*)` | Data exfiltration |
| Critical | `Bash(gh auth:*)` | Authentication hijacking |
| Critical | `Bash(git filter-branch:*)` | Destructive history rewriting |
| Critical | `Bash(git reset:*)` | Can destroy uncommitted work |
| High | `Bash(gh api:*)` | Unrestricted GitHub API access |
| High | `Bash(git config:*)` | Can set malicious hooks paths |
| High | `Bash(git remote set-url:*)` | Can redirect pushes |
| High | (empty deny list) | No safety guardrails |

**How permissions accumulate:** Project `settings.json` grows over time as users approve Claude's permission prompts during sessions. It's easy to approve something risky in the moment when you're focused on the task, not thinking about the permanent permission being granted. Over time, dangerous permissions like `python:*` and `curl:*` accumulate. The audit catches this drift.

### Step 2: Generate Blog Content

Using the scan results, generate the blog post content by:

1. Read the template from `assets/blog_template.md`
2. Fill in placeholders with actual configuration data:
   - `{DATE}` - Current date in ISO format
   - `{GLOBAL_SETTINGS}` - Formatted global settings
   - `{ENABLED_PLUGINS}` - List of enabled plugins with descriptions
   - `{MCP_SERVERS}` - MCP server configurations
   - `{INSTALLED_SKILLS}` - List of custom skills
   - `{PROJECT_SETTINGS}` - Project-specific settings
   - `{HOOKS}` - Claude and git hooks
   - `{SETUP_INSTRUCTIONS}` - Step-by-step replication guide
   - `{WORKFLOWS}` - Common workflows and tips
   - `{RATIONALE}` - Explanation of configuration choices

3. Write to `content/posts/my-claude-setup.md` in the Hugo site

### Step 3: Create or Update Pull Request

**First, check for existing PR:**
```bash
gh pr list --search "claude setup" --state open --json number,headRefName,title
```

**If an existing PR exists:**
1. Check out the existing branch: `git checkout <branch-name>`
2. Pull latest changes: `git pull`
3. Make your updates to the blog post
4. Commit with message describing what changed
5. Push to the existing branch: `git push`
6. The existing PR will be updated automatically

**If no existing PR:**
1. Create a new git branch: `update-claude-setup-{timestamp}`
2. Commit the changes with message:
   ```
   docs: update Claude Code setup documentation

   Auto-generated update of Claude Code configuration blog post.

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
   ```
3. Push the branch
4. Create a PR using `gh pr create`

**Important:** Never have more than one open PR. Always reuse existing PRs if one exists.

### Step 4: Self-Improve the Skill

After generating the blog post, review what you learned during the process and update this skill if needed.

**Ask yourself:**
- Did web searches reveal new Claude Code features not covered in this skill?
- Did documentation show better ways to explain concepts?
- Are there new best practices that should be incorporated?
- Did you discover new configuration options worth documenting?
- Are any instructions in this skill outdated?

**If yes to any of the above:**
1. Update `.claude/skills/claude-setup-blog/SKILL.md` with the new knowledge
2. Add updates to the "Documentation Links" section if new URLs were found
3. Update example formats if better patterns were discovered
4. Include SKILL.md changes in the same commit/PR as the blog post update

**What to update:**
- New features → Add to "Required explanations" list
- New URLs → Update "Documentation Links" section
- Better explanation patterns → Update example formats
- Deprecated features → Remove or mark as deprecated
- New configuration options → Add to scanner output documentation

**Example:** If you discover Claude Code now has a "themes" feature, add it to the required explanations list and document how to scan for theme configurations.

This keeps the skill evergreen and improves with each run.

## Content Generation Guidelines

### Beginner-Friendly Explanations (For Features You Use)

Only explain features that are **actually configured in your setup**. This is a personal setup post, not a Claude Code tutorial.

**Rule:** If you're using it → explain it briefly with a doc link. If you're not using it → just note "Not currently configured" with a link for readers who want to learn more.

**For features you ARE using:**
```markdown
### Plugins

**What are plugins?** Plugins extend Claude Code with specialized capabilities. [Learn more →](https://docs.anthropic.com/...)

I have the following plugins enabled:
- **document-skills** - I use this for...
```

**For features you're NOT using:**
```markdown
### MCP Servers

I don't currently use MCP servers. [Learn about MCP →](https://modelcontextprotocol.io/)
```

**Keep it focused:** The blog post documents YOUR setup, not all possible Claude Code features. Only go deep on things you actually use and can speak to from experience.

### Copy-Friendly Setup

Make it **extremely easy** to replicate the setup. Requirements:

1. **Single copy-paste blocks** - Each config file should be a complete, standalone code block that can be copied and pasted directly
2. **No `...` or truncation** - Show the FULL configuration, not abbreviated versions
3. **Include file paths** - Always show where the file should be saved
4. **Sequential numbered steps** - Clear 1, 2, 3 order for setup
5. **Verification commands** - After each step, show how to verify it worked

**Example format:**
```markdown
**Step 1: Create global settings**

Save this to `~/.claude/settings.json`:
```json
{
  "model": "sonnet",
  "enabledPlugins": {
    "document-skills@anthropic-agent-skills": true,
    ...full config...
  }
}
```

Verify: `cat ~/.claude/settings.json`
```

### Writing Style

Use **technical documentation style**:
- Clear, concise, code-focused
- Include code snippets and examples
- Use bullet points and lists for readability
- Add inline code formatting for commands and file paths

### Required Sections

Every blog post must include these sections:

1. **Overview** - Brief intro with "Browse my config files" quick links:
   ```markdown
   **Browse my config files:**
   - [CLAUDE.md](.claude/CLAUDE.md) — My global instructions for Claude
   - [Project settings](.claude/settings.local.json) — Permissions for this repo
   - [claude-setup-blog skill](.claude/skills/claude-setup-blog/) — The skill that generates this post
   ```

2. **CLAUDE.md** - Explain what CLAUDE.md is, link to yours, summarize key points:
   ```markdown
   ## CLAUDE.md

   **What is CLAUDE.md?** A special file that Claude automatically pulls into context... [Learn more →](docs-link)

   **My CLAUDE.md:** [View file →](github-link-to-your-file)

   Key things I tell Claude:
   - Bullet point summaries of your CLAUDE.md content
   ```

3. **Plugins** (table format with hyperlinked names):
   | Plugin | What I Use It For |
   |--------|-------------------|
   | [**document-skills**](https://github.com/anthropics/skills) | Creating DOCX, PDF files |

4. **Skills** (table format with sources)

5. **Permissions** - Global and project permissions with code blocks

6. **MCP Servers** - Even if empty, note "Not currently configured" with doc link

7. **Hooks** - Even if empty, note "Not currently configured" with doc link

8. **How to Replicate My Setup** - Step-by-step numbered instructions

9. **Workflows I Use Daily** - Practical usage examples

10. **Files in This Repo** - Table linking to all Claude config files:
    | File | Description |
    |------|-------------|
    | [.claude/CLAUDE.md](github-link) | My global Claude instructions |

11. **Resources** - Links to official documentation

12. **Changelog** - Release notes with PR links

### Sections to Generate

**Global Settings**: Show configuration as formatted code blocks:
```json
{
  "model": "sonnet",
  "enabledPlugins": { ... }
}
```

**Enabled Plugins**: Use table format with hyperlinked plugin names (no separate Source column):
| Plugin | What I Use It For |
|--------|-------------------|
| [**document-skills**](https://github.com/anthropics/skills) | Document creation and editing (DOCX, PDF, XLSX, etc.) |
| [**frontend-design**](https://github.com/anthropics/claude-plugins-official) | Build beautiful web interfaces |

**MCP Servers**: Document each configured server:
```json
{
  "github": {
    "url": "https://api.githubcopilot.com/mcp/",
    "status": "connected"
  }
}
```

**Setup Instructions**: Provide step-by-step commands for replication:
```bash
# 1. Install Claude Code
npm install -g @anthropic-ai/claude-code

# 2. Configure settings
mkdir -p ~/.claude
cat > ~/.claude/settings.json << 'EOF'
{...}
EOF

# 3. Install plugins
claude plugin install document-skills
```

**Workflows & Tips**: Share practical usage examples:
- "Use `/commit` to automatically stage changes and create semantic commits"
- "Run `/code-review <PR-number>` to get AI-powered code reviews"

**Rationale**: Explain why you chose specific configurations:
- "I use Sonnet as the default model for the best balance of speed and capability"
- "The document-skills plugin is essential for working with various file formats"

## Handling Edge Cases

### First-Time Creation

If `content/posts/my-claude-setup.md` doesn't exist:
1. Use the full template from `assets/blog_template.md`
2. Create the file with all sections populated
3. Set `draft: false` to publish immediately

### Updating Existing Post

If the post already exists:
1. Read the existing file
2. Parse the frontmatter to preserve custom fields
3. Replace only the content sections, keeping the structure
4. Update the `date` field to current timestamp
5. Preserve any custom sections added manually

### Empty Configuration

If certain configurations are empty (no MCP servers, no custom skills):
- Show a placeholder message: "No MCP servers currently configured"
- Provide links to documentation for adding them
- Don't skip the section entirely

## Changelog Format

The changelog follows a **release notes style** similar to software projects. Each update is a versioned entry with PR links.

### Structure

```markdown
## Changelog

### YYYY-MM-DD ([PR #N](https://github.com/jamesrappazzo/personal-website/pull/N))

**Added**
- New feature or configuration item
- Another new item

**Changed**
- Modified behavior or configuration

**Removed**
- Deleted configuration or feature

**Fixed**
- Bug fix or correction
```

### Guidelines

1. **Date format**: ISO 8601 (YYYY-MM-DD)
2. **PR link**: Always link to the PR that introduced the changes
3. **Categories**: Use standard changelog categories:
   - **Added** - New configurations, plugins, permissions, or features
   - **Changed** - Modifications to existing configurations
   - **Removed** - Deleted or disabled configurations
   - **Fixed** - Corrections to documentation or configuration errors
4. **Entry style**:
   - Start with action verb (Add, Update, Remove, Fix)
   - Be specific but concise
   - Group related changes under one bullet when appropriate
5. **Order**: Newest entries at the top
6. **Omit empty categories**: Only include categories that have changes

### Example Entry

```markdown
### 2026-01-15 ([PR #5](https://github.com/jamesrappazzo/personal-website/pull/5))

**Added**
- MCP server for GitHub Copilot integration
- New permission for Bash(docker:*)

**Changed**
- Updated default model from Sonnet to Opus for complex tasks

**Removed**
- Deprecated typescript-lsp plugin (now built-in)
```

## Blog Style Guide

### Voice & Tone

- **First person**: "I use...", "My configuration...", "I prefer..."
- **Technical but approachable**: Assume readers are developers but explain the "why"
- **Practical focus**: Emphasize real-world usage over theoretical benefits

### Code Blocks

- **Show full configs** for things users would copy (settings.json, permissions)
- **Use syntax highlighting**: Always specify language (json, bash, etc.)
- **Add comments** in bash scripts for clarity

### Sections

- **Headers**: Use `##` for main sections, `###` for subsections
- **Lists**: Use bullet points for features/items, numbered lists for steps
- **Bold**: Use for emphasis on key terms, plugin names, and categories
- **Inline code**: Use backticks for file paths, commands, and config keys

### Content Principles

1. **Show, don't just tell**: Include actual config snippets, not just descriptions
2. **Explain rationale**: Each major choice should have a "why" explanation
3. **Keep it current**: Remove outdated information, don't just append
4. **Replication-friendly**: A reader should be able to copy your setup from this post

### Linking Requirements

**CRITICAL:** Every external tool, plugin, or resource mentioned MUST link to its official source.

1. **Plugins**: Hyperlink plugin names directly to their GitHub repos (no separate Source column)
   - Official plugins → `https://github.com/anthropics/claude-plugins-official`
   - Document skills → `https://github.com/anthropics/skills`

2. **Config Files in Repo**: Link to the actual files in your GitHub repo
   - Use format: `[.claude/CLAUDE.md](https://github.com/username/repo/blob/main/.claude/CLAUDE.md)`
   - Include a "Files in This Repo" table at the bottom

3. **Documentation**: Link to official docs for each Claude Code feature explained
   - Use arrow format: `[Learn more →](url)`

4. **Skills**: Include Source column linking to skill location in repo

5. **Quick Links**: Add "Browse my config files" links at the top of Overview section

## Documentation Links

When generating the blog post, include these links (verified February 2026):

**Core Documentation:**
- Claude Code overview: `https://code.claude.com/docs/en/overview`
- Claude Code best practices: `https://www.anthropic.com/engineering/claude-code-best-practices`
- CLAUDE.md / Memory guide: `https://code.claude.com/docs/en/memory`
- Extend Claude Code (features overview): `https://code.claude.com/docs/en/features-overview`

**Feature-Specific:**
- Plugins: `https://code.claude.com/docs/en/plugins`
- Plugins reference (technical): `https://code.claude.com/docs/en/plugins-reference`
- Plugin marketplaces: `https://code.claude.com/docs/en/plugin-marketplaces`
- Skills: `https://code.claude.com/docs/en/skills`
- Subagents: `https://code.claude.com/docs/en/sub-agents`
- Agent teams: `https://code.claude.com/docs/en/agent-teams`
- Settings & Permissions: `https://code.claude.com/docs/en/settings`
- MCP servers: `https://code.claude.com/docs/en/mcp`
- Hooks guide (practical): `https://code.claude.com/docs/en/hooks-guide`
- Hooks reference (technical): `https://code.claude.com/docs/en/hooks`

**External Resources:**
- Model Context Protocol: `https://modelcontextprotocol.io/`
- Full docs index: `https://code.claude.com/docs/llms.txt`

**Plugin Sources (GitHub repos):**
- Official plugins: `https://github.com/anthropics/claude-plugins-official`
- Document skills (xlsx, docx, pdf, pptx): `https://github.com/anthropics/skills`
- Claude Code repo: `https://github.com/anthropics/claude-code`

**Plugin Installation:**
To install plugins, users should:
1. Add marketplace: `/plugin marketplace add anthropics/claude-plugins-official`
2. Browse and enable via `/plugin` menu
3. Or add directly to `~/.claude/settings.json` under `enabledPlugins`

**Important:** URLs change. Always verify links are valid via WebSearch before including them.

## Resources

### scripts/scan_claude_config.py

Python script that scans Claude configuration and outputs JSON. Functions:
- `scan_settings()` - Read global settings files
- `scan_mcp_servers()` - Read MCP configuration
- `scan_skills()` - List installed skills
- `scan_hooks()` - Find Claude and git hooks
- `scan_project_settings()` - Read project-specific settings
- `audit_permissions()` - Check all permission sources for security risks
- `generate_config_report()` - Combine all scans into one report (includes audit)

Can be run standalone or imported as a module.

**CLI flags:**
- `--audit` - Run permissions audit only (human-readable output)
- `--dry-run` - Show sanitization config + full report preview
- `--show-config` - Show sanitization configuration
- (no flags) - Generate full JSON report

### assets/blog_template.md

Hugo-compatible markdown template with placeholders for:
- Frontmatter (title, date, tags, categories)
- Configuration sections
- Setup instructions
- Workflows and tips

## Installation

### Option 1: Install to Global Skills (for personal use)

```bash
claude skill install claude-setup-blog.skill
```

### Option 2: Add to Website Repo (to share with others)

To make this skill part of your open-source website so others can use it:

```bash
# From your personal-website repo
mkdir -p .claude/skills
cp -r /path/to/claude-setup-blog .claude/skills/
git add .claude/skills/claude-setup-blog
git commit -m "feat: add Claude setup blog generator skill"
```

This allows others who clone your website repo to use the same skill to document their own setups.

## Usage

Invoke the skill by asking:
- "Update my Claude setup blog post"
- "Generate my Claude Code documentation"
- "Document my current Claude configuration"
- "Scan my setup and create a PR to my website"

The skill will:
1. Scan your configuration
2. Generate/update the blog post
3. Create a PR for review
4. Provide the PR URL for you to merge

## Example Output

After running, you'll get:
- Updated `content/posts/my-claude-setup.md` in your Hugo site
- A new git branch with the changes
- A PR with description of what was updated
- The PR URL to review and merge

The blog post will be automatically published on your website after merging the PR (via your GitHub Actions workflow).
