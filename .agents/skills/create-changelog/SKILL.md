---
name: create-changelog
description: Create or update a release changelog from repository evidence. Use for release notes, CHANGELOG.md updates, version summaries, or user-facing descriptions of changes between refs.
---

# Create Changelog

Produce a concise changelog that users can trust.

## Determine the source range

Use the range supplied by the user. Otherwise inspect tags, releases, branch history, and the existing changelog to identify the most defensible range. State the chosen range when ambiguity remains. Never treat commit subjects alone as proof of user-facing behavior; inspect material diffs when needed.

## Build the changelog

- Preserve the repository's existing format. If none exists, use a Keep a Changelog-style `Unreleased` section with only relevant categories: `Added`, `Changed`, `Fixed`, `Deprecated`, `Removed`, and `Security`.
- Describe user-visible outcomes in plain language. Consolidate related commits and omit merges, formatting-only work, and internal noise unless it matters to operators.
- Call out breaking changes, required migrations, configuration changes, compatibility constraints, and security fixes prominently.
- Include issue, PR, or contributor references only when repository evidence supplies them.
- Use a release date only when the release actually occurred or the user provided one; otherwise keep changes under `Unreleased`.
- Do not invent versions, dates, performance claims, vulnerability identifiers, or fixed behavior.

When editing `CHANGELOG.md`, avoid duplicating represented entries and preserve historical sections unchanged. Report the source range and any commits intentionally excluded.
