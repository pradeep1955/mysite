# Agent / Skill Guidance

This repository ships a Claude Code skill for optimising the `mysite` Django project.

- Location: `.claude/skills/django-optimize/SKILL.md`
- Skill name: `django-optimize`

## How Claude Code discovers it

Claude Code auto-loads skills from `.claude/skills/<name>/SKILL.md` (project-level)
or `~/.claude/skills/<name>/SKILL.md` (user-level). The skill is selected by Claude
when the `description` in its frontmatter matches the user's request, or when the
user invokes it explicitly via `/django-optimize`.

No copy/paste into any external UI is needed — just keep the file in place.

## Example prompts that should trigger it

- "Audit `mysite/settings.py` for production readiness on Render."
- "Find N+1 query patterns in the `blog` and `news` apps."
- "What's safe to drop from `requirements.txt`?"
- "Harden security headers for production."
- "Optimise the home page — it's slow."

## Scope

The skill is focused on **optimisation and production-readiness**:

- Performance: query patterns, caching, pagination, indexing, template hotspots.
- Security: `DEBUG`, `ALLOWED_HOSTS`, secrets handling, HTTPS/HSTS headers.
- Deployment: Render config (`render.yaml`), static/media file delivery, `collectstatic`.
- Code quality: dead config, unused dependencies, apps on disk but not installed.

For broader changes (new features, large refactors), prefer a normal conversation
without invoking the skill.
