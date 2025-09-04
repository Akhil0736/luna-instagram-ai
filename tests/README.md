# Luna Unified Tests

This directory hosts the unified testing setup for Luna across Python and TypeScript/frontend components.

- Python tests use `pytest`.
- TypeScript/frontend tests use `Jest`.

## Structure

- `python/` — Pytest configuration and tests that target Python components (e.g., `openmanus/`).
- `js/` — Jest configuration and tests that target TypeScript/JavaScript components (e.g., `frontend/`, `riona/`).

## Quickstart

### Python (pytest)

1. Ensure Python 3.10+ is available.
2. Install dev dependencies in your Python environment:
   - `pip install -r openmanus/requirements.txt` (if applicable)
   - `pip install pytest`
3. Run tests using the local config:
   - `pytest -c tests/python/pytest.ini`

### TypeScript/Frontend (Jest)

1. Ensure Node.js 18+ and pnpm/npm/yarn are available.
2. From project root, install test deps in your frontend workspace(s) as needed:
   - In `frontend/` and/or `riona/`: install `jest`, `ts-jest`, `@types/jest`, and `typescript` if not already present.
3. Run tests using the local config:
   - `npx jest -c tests/js/jest.config.js`

Adjust paths in the configs if your repo layout changes.
