# vc-auto-tests

Automated test suite for VC, built with [Playwright](https://playwright.dev/python/) and pytest.

## Requirements

- Python 3.13+
- Git

## Installation

### 1. Clone the repository

```bash
git clone <repo-url>
cd vc-auto-tests
```

### 2. Create and activate a virtual environment

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -e .
```

### 4. Install Playwright browsers

```bash
playwright install
```

## Seeding test data

The test dataset is seeded into the backend via WebAPI. Run this once against a
fresh environment (and whenever the dataset changes):

```bash
python -m dataset.dataset_manager --seed --mode ci
```

Pass entity names to seed only a subset (order is taken from the manifest, not
the command line):

```bash
python -m dataset.dataset_manager --seed stores pages pages_content
```

### Post-seeding scripts

Some entities need a follow-up action that the create API cannot express
directly — a state transition, a workflow trigger, etc. These live in
`dataset/scripts/` and are run **after** seeding, on demand.

| Script | Purpose | Command |
| --- | --- | --- |
| `set_builder_page_status` | Page-builder pages are always seeded as `Draft` (publish/archive is a backend workflow, not a settable field). This script transitions one page to a target status. | `python -m dataset.scripts.set_builder_page_status --page-id <id> --status <Published\|Archived>` |

> **Note:** seeding leaves every page in `Draft`. To publish or archive a page,
> run `set_builder_page_status` with its grouped page **id** (the stable key the
> API uses — page names are not guaranteed unique):
>
> ```bash
> python -m dataset.dataset_manager --seed --mode ci
> python -m dataset.scripts.set_builder_page_status --page-id acme-store-grouped-page-about-store --status Published
> python -m dataset.scripts.set_builder_page_status --page-id acme-store-grouped-page-legacy-catalog --status Archived
> ```

The seed command accepts `--mode dev` (default, per-item detail) or `--mode ci`
(summary output); `set_builder_page_status` accepts the same `--mode` flag.

## Running Tests

```bash
pytest
```
