---
name: review-changes-pr
description: Review a local change set, commit range, branch, or pull request for actionable defects and risks. Use when the user asks for code review, PR review, change validation, or merge-readiness feedback.
---

# Review Changes or PR

Perform an evidence-based review that prioritizes correctness over commentary volume.

## Establish the review target

- Determine the intended base and head from the request, PR metadata, or repository state. State the comparison used when it is not obvious.
- Read repository instructions and inspect the complete diff plus enough surrounding code to understand behavior.
- Identify the stated goal and acceptance criteria. A change can be internally consistent yet still fail its purpose.

## Review priorities

Look for issues that can cause observable harm:

- incorrect behavior, missing edge cases, or violated business rules;
- data loss, concurrency errors, unsafe migrations, or broken transaction boundaries;
- security, privacy, authorization, input-validation, and secret-handling problems;
- API, schema, configuration, deployment, or backward-compatibility breaks;
- resource leaks, severe performance regressions, and unreliable failure handling;
- tests that are missing for material behavior or pass without exercising the change.

Run focused checks when they can confirm or disprove a suspected defect. Do not change the implementation during a review unless the user also asks for fixes.

## Output

List findings first, ordered by severity. For every finding include severity (`Critical`, `High`, `Medium`, or `Low`), trigger conditions, affected file and line, impact, and a correction direction when useful.

Avoid style-only observations unless they impair correctness or maintenance. Do not invent findings to fill a quota. If no actionable defects are found, say so and mention remaining verification gaps or risks. Provide a short overall assessment after the findings.

Creating review comments, approvals, change requests, or other GitHub mutations requires an explicit user request.
