# Shared Module

Cross-repo utilities and type definitions for Luna.

## Structure

- `utils/` — Common helper functions used by multiple components.
  - `python/` — Python utilities importable via `shared.utils.python`.
  - `typescript/` — TypeScript utilities importable via `shared/utils/typescript`.
- `types/` — Shared type definitions.
  - `python/` — Python types (e.g., `TypedDict`/`dataclasses`).
  - `typescript/` — TypeScript interfaces and types.

When adding shared code, keep it framework-agnostic and well-documented.
