---
name: create-prd
description: Create a clear, shareable Product Requirements Document from a supplied problem statement. Use when the user wants a PRD, requirements specification, interview document, or structured product plan grounded in the source statement.
---

# Create Prd

Transform the problem statement into a decision-ready PRD without inventing requirements or hiding uncertainty.

## Interpret the source

1. Read the complete problem statement and any repository context the user placed in scope.
2. Separate source-backed facts into: problem, actors, desired outcomes, constraints, business rules, required data, and explicit acceptance conditions.
3. Identify contradictions, missing decisions, and ambiguous terms. Ask only when an unresolved choice would materially change the product; otherwise make a conservative assumption and label it.
4. Distinguish requirements from implementation suggestions. Preserve technology or delivery choices only when the user made them requirements.

## Build the PRD

Adapt the document to the product instead of filling a rigid template. Include the sections that aid decisions, normally:

- title, version or status, and intended audience;
- executive summary and problem statement;
- goals, success criteria, and non-goals;
- users, actors, and primary use cases;
- functional requirements with stable identifiers;
- business rules, workflows, state transitions, and error behavior;
- data requirements and API or interface expectations when applicable;
- non-functional requirements that follow from the problem, such as security, consistency, scale, availability, accessibility, or compliance;
- acceptance criteria traceable to requirements;
- dependencies, assumptions, constraints, risks, and open questions;
- release scope, validation approach, and an appropriate future roadmap.

Use tables when they make mappings or traceability easier to scan. Use Mermaid or PlantUML only when a workflow, state model, architecture, or relationship is materially clearer as a diagram.

## Evidence and precision

- Mark each inferred detail as an assumption; never present it as source-provided fact.
- Avoid fabricated metrics, dates, budgets, personas, integrations, compliance obligations, or technical scale.
- Convert vague words such as "fast," "secure," or "user-friendly" into measurable criteria only when evidence supports a target. Otherwise record the measurement as an open decision.
- Make acceptance criteria observable and testable. Prefer concrete inputs, actions, states, and outcomes.
- Keep identifiers consistent so tests and implementation tasks can reference them.
- Call out conflicts rather than silently resolving them.

## Repository output

When the user asks for a Markdown artifact, follow the repository's documentation conventions and choose a discoverable name such as `docs/PRD.md`. Preserve an existing PRD's useful history and structure when updating it. Link relevant local designs or API documents instead of duplicating large sections.

Finish with a concise summary of source coverage, labeled assumptions, and unresolved decisions. Do not implement the product, create tickets, publish documents, or mutate external systems unless the user separately requests those actions.
