---
name: regression-test
description: Plan and execute risk-based regression testing after code or configuration changes. Use when the user wants confidence that existing behavior still works or asks for a regression suite or report.
---

# Regression Test

Verify that a change has not damaged behavior outside its intended scope.

## Build the regression scope

1. Inspect the change set, dependency/configuration updates, affected call paths, and public interfaces.
2. Map direct changes to downstream consumers and identify high-risk shared components, data paths, and failure modes.
3. Select tests in layers: changed-module tests first, then integration or contract tests for affected boundaries, then the broader suite when cost is proportionate.
4. Include past bug tests and important business invariants when the repository makes them discoverable.

## Execute safely

- Use documented commands and isolated test data or environments.
- Separate setup failures from product failures; do not label an unexecuted test as passed.
- Reproduce failures once when safe, capture useful error evidence, and identify whether a failure is new, pre-existing, or environment-related when evidence permits.
- Do not update snapshots, baselines, golden files, or expected results merely to make a failure disappear.
- Do not modify production code during a testing-only request. Add or repair tests only when the user asks for test implementation.

## Report

Summarize the examined change range, commands run, tests passed, failed, or skipped, coverage when available, discovered regressions, and untested risks. A green suite is not proof of no regression; state material gaps such as unavailable services, missing data, platform differences, or absent coverage.
