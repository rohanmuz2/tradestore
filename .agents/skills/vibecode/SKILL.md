---
name: vibecode
description: Turn a product idea or loosely specified feature into a working, verified implementation. Use for rapid idea-to-code requests where Codex should infer safe details, build an end-to-end slice, and keep the result maintainable.
---

# Vibecode

Convert the user's intended outcome into the smallest complete implementation that is useful, testable, and easy to extend.

## Workflow

1. Inspect the repository, local instructions, current behavior, and available test/build commands before choosing an approach.
2. Turn the request into observable outcomes. Make reversible, low-risk assumptions when details are missing; ask only when a choice would materially change the product.
3. Follow the repository's existing architecture and conventions. Prefer a vertical slice that works end to end over disconnected scaffolding.
4. Implement the requested experience, including relevant validation, error handling, persistence, and configuration. Do not add speculative features.
5. Add or update tests around business behavior and important boundaries. Run focused checks while iterating, then the relevant full suite before handoff.
6. Review the final diff for accidental changes, secrets, generated artifacts, debug code, and incomplete placeholders.
7. Report what works, how it was verified, assumptions that affect behavior, and any genuine remaining limitation.

## Guardrails

- Preserve existing user changes and public interfaces unless the request requires changing them.
- Prefer established dependencies. Add one only when its value outweighs its maintenance and security cost.
- Keep credentials and environment-specific values out of source control.
- Do not publish, deploy, message people, or mutate external systems unless the user requested that action.
- If a prototype shortcut would be unsafe in production, make that boundary explicit rather than presenting it as production-ready.
