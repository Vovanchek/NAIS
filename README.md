# Test Me Automation

Risk-based UI and API automation for the published training storefront at `https://test-me.vzl.one/`.

## Stack

- Python 3.11+
- pytest
- Selenium 4
- Requests
- Ruff
- pytest-xdist for controlled API parallelism

## Coverage

The suite prioritizes workspace isolation, catalog contracts, quote calculations in integer kopecks, approved/declined order flows, cancellation, reviews, favorites and the critical browser checkout journey.

Documentation:

- [Test plan](docs/test-plan.md)
- [Detailed test cases](docs/test-cases.md)
- [Automation traceability](docs/traceability.md)
- [Confirmed defects](docs/defects.md)
- [Execution report template](docs/execution-report.md)

## Installation

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -c constraints.txt -e ".[dev]"
```

### Git Bash

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -c constraints.txt -e ".[dev]"
```

## Configuration

All settings are optional and have safe defaults for the assignment environment.

```text
BASE_URL=https://test-me.vzl.one
BROWSER=chrome
HEADLESS=true
API_CONNECT_TIMEOUT=5
API_READ_TIMEOUT=20
ARTIFACT_DIR=artifacts
```

The configuration rejects non-HTTPS URLs, unexpected hosts, credentials in URLs, query strings, fragments and non-root paths.

## Quality gates

```bash
python -m ruff format --check .
python -m ruff check .
python -m pytest --collect-only -q
python -m pytest tests/unit -q
```

## Test execution

Green API release gate, excluding confirmed product defects:

```bash
python -m pytest -m "api and not known_defect" -q
```

Confirmed defect contracts:

```bash
python -m pytest -m known_defect -q
```

Critical browser smoke:

```bash
python -m pytest -m "ui and smoke" -q
```

All UI tests:

```bash
python -m pytest -m ui -q
```

Controlled API parallel run:

```bash
python -m pytest -m "api and not known_defect" -n 2 --dist loadscope -q
```

Do not use a large worker count because the public environment enforces write-rate limits.

## Known defects

Confirmed application defects use both:

- `@pytest.mark.known_defect`
- `@pytest.mark.xfail(strict=True, reason="TM-DEF-...")`

This keeps the normal release gate green while making an unexpected fix produce a strict XPASS that requires review. Full reproduction details and evidence references are in `docs/defects.md`.

## Failure artifacts

On a UI failure, the framework attempts to write the following under a sanitized test-specific directory:

```text
artifacts/<test-id>/
├── screenshot.png
├── page_source.html
└── failure.txt
```

Artifact collection is best-effort and cannot replace the original test exception. Workspace tokens and common sensitive values are redacted. `artifacts/` is excluded from Git.

## CI

`.github/workflows/quality-gates.yml` runs formatting, lint, collection, unit tests and the green API release gate. Known-defect checks run separately and do not hide first-attempt results.

UI execution is intentionally not a blocking pull-request job because the public browser environment may be unavailable or rate limited. Run UI smoke locally and record the result in `docs/execution-report.md`.

## Repository hygiene

Before pushing:

```bash
git status --short
git ls-files | grep -E '(__pycache__|\.pyc$|\.egg-info)'
```

The second command must return no tracked generated files. Never commit `.env`, workspace tokens, cookies, browser profiles, screenshots with personal data, or generated reports.

## Publishing changes

```bash
git switch -c framework-improvements
git add .
git commit -m "Improve automation reliability and traceability"
git push -u origin framework-improvements
```
