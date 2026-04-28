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

## Running Tests

```bash
pytest
```
