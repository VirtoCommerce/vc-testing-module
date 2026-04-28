# vc-auto-tests

Automated test project using Playwright + pytest.

## Project Overview

End-to-end test suite for VC. Tests live in `tests/`. Configuration is in `pyproject.toml`.

## Commands

```bash
# Install dependencies
pip install -e .

# Install Playwright browsers
playwright install

# Run all tests
pytest

# Run a specific test file
pytest tests/test_example.py

# Run tests in headed mode
pytest --headed
```

## Architecture

- `tests/` — test files
- `gql/operations/` — GraphQL operation files (.graphql)
- `gql/types/` — ariadne-codegen generated typed client (do not edit manually)
- `core/` — shared infrastructure (auth, clients, logger, settings)
- `dataset/` — dataset management and seeding
- `pyproject.toml` — dependencies, pytest config, ariadne-codegen config
