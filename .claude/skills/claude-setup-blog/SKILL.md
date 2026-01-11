---
name: claude-setup-blog
description: Automatically scan Claude Code configuration (settings, MCP servers, skills, hooks) and generate or update a blog post documenting the setup with installation instructions for others. Use when the user wants to document their Claude setup, update their setup documentation, or create a blog post about their Claude Code configuration. Triggered by requests like "update my Claude setup blog post", "document my Claude configuration", or "generate my setup documentation".
---

# Claude Setup Blog Generator

Automatically scans your Claude Code configuration and generates/updates a blog post documenting your setup for others to learn from and replicate.

## Overview

This skill helps you maintain an evergreen blog post about your Claude Code setup by:

1. Scanning your Claude configuration files (settings, MCP servers, skills, hooks)
2. Generating or updating a blog post in your Hugo website
3. Creating a pull request with the changes

The blog post includes:
- Your configuration settings
- Enabled plugins and skills
- MCP server configurations
- Hooks and automations
- Instructions for others to replicate your setup
- A changelog tracking all updates with PR links

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

After updating the blog post, check for an existing open PR before creating a new one:

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
4. Create a PR using `gh pr create` with description explaining what changed

**Important:** Never have more than one open PR for the Claude setup blog at a time. Always reuse an existing PR if one is open.

## Content Generation Guidelines

### Beginner-Friendly Explanations

Every major concept MUST include a brief explanation for newcomers. Assume the reader may not know what these things are:

**Required explanations (with official doc links):**

- **What is Claude Code?** - Brief intro (1-2 sentences) + link to official docs
- **What are Plugins?** - Explain that plugins extend Claude's capabilities with specialized tools. Link to plugin docs.
- **What are MCP Servers?** - Explain Model Context Protocol - how Claude connects to external services. Link to modelcontextprotocol.io
- **What are Skills?** - Explain custom reusable prompts/workflows. Link to skills docs.
- **What are Hooks?** - Explain automated actions triggered by events. Link to hooks docs.
- **What are Permissions?** - Explain the allow/deny/ask system for tool access. Link to permissions docs.

**Format for explanations:**
```markdown
### Plugins

**What are plugins?** Plugins extend Claude Code with specialized capabilities - from document editing to code review. They're like apps for Claude. [Learn more →](https://docs.anthropic.com/...)

I have the following plugins enabled:
...
```

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

### Sections to Generate

**Global Settings**: Show configuration as formatted code blocks:
```json
{
  "model": "sonnet",
  "enabledPlugins": { ... }
}
```

**Enabled Plugins**: List each plugin with brief description:
- `document-skills` - Document creation and editing (DOCX, PDF, XLSX, etc.)
- `frontend-design` - Build beautiful web interfaces
- `github` - GitHub integration and PR management
- etc.

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

## Documentation Links

When generating the blog post, include these links (verify via WebSearch that URLs are current):

**Core Documentation:**
- Claude Code main docs: `https://docs.anthropic.com/en/docs/claude-code`
- Claude API docs: `https://docs.anthropic.com/`

**Feature-Specific:**
- Plugins: Search for current URL
- MCP: `https://modelcontextprotocol.io/`
- Skills: Search for current URL
- Hooks: Search for current URL
- Permissions: Search for current URL

**Important:** URLs change. Always verify links are valid before including them. Use WebSearch to find the current official documentation for each feature.

## Resources

### scripts/scan_claude_config.py

Python script that scans Claude configuration and outputs JSON. Functions:
- `scan_settings()` - Read global settings files
- `scan_mcp_servers()` - Read MCP configuration
- `scan_skills()` - List installed skills
- `scan_hooks()` - Find Claude and git hooks
- `scan_project_settings()` - Read project-specific settings
- `generate_config_report()` - Combine all scans into one report

Can be run standalone or imported as a module.

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
