# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About Me

I'm James, a web developer working primarily with TypeScript.

## Tech Stack

- **Frontend**: React, Next.js, Tailwind CSS
- **Backend**: Node.js, Next.js API routes
- **Database**: Prisma ORM
- **Testing**: Jest or Vitest

## Git Workflow

For each distinct task:

1. **Setup**: Initialize git repo if needed, then create a new feature branch
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
- When working with Next.js, follow App Router patterns unless the project uses Pages Router
- Use Prisma's type-safe queries and leverage generated types
