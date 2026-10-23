---
name: functional-test
description: Validate implemented behavior against product requirements and acceptance criteria through black-box or API-level testing. Use for functional test planning, execution, evidence, or test-case creation.
---

# Functional Test

Test what the system does from the consumer's perspective rather than its internal implementation.

## Derive expected behavior

- Read the requirement, acceptance criteria, API contract, and relevant user documentation.
- Convert each requirement into observable preconditions, actions, and expected results.
- Mark ambiguities instead of silently choosing an expectation that changes product meaning.

## Design cases

Cover the smallest set that gives meaningful behavioral confidence:

- primary successful workflows;
- input and state boundaries;
- invalid input and business-rule rejection;
- repeated, duplicate, or idempotent actions when relevant;
- state transitions and persistence across requests;
- authorization and role differences when present;
- externally visible error responses and recovery.

Keep each case traceable to a requirement. Avoid duplicating unit-level implementation tests unless the behavior is visible through the public interface.

## Execute and report

Use an isolated environment and disposable data. Record the environment, exact action or command, expected result, actual result, and pass/fail status. Preserve concise failure evidence and distinguish product defects from environment or test-data problems.

Do not mutate production services or third-party systems without explicit authorization. In a testing-only request, report defects rather than changing application behavior. If the user asks to implement automated functional tests, follow the repository's existing framework and ensure the tests are deterministic, independent, and suitable for CI.
