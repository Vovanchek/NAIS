# Test Execution Report

Complete this file after the final run. Do not claim a check passed unless it was executed successfully.

## Environment

- Date/time (UTC):
- Commit SHA:
- Operating system:
- Python version:
- Browser/version:
- Headless:
- Base URL: `https://test-me.vzl.one`

## Results

| Command | Passed | Failed | Xfailed | Xpassed | Skipped | Duration |
|---|---:|---:|---:|---:|---:|---:|
| `python -m ruff format --check .` | | | | | | |
| `python -m ruff check .` | | | | | | |
| `python -m pytest --collect-only -q` | | | | | | |
| `python -m pytest tests/unit -q` | | | | | | |
| `python -m pytest -m "api and not known_defect" -q` | | | | | | |
| `python -m pytest -m known_defect -q` | | | | | | |
| `python -m pytest -m "ui and smoke" -q` | | | | | | |

## Confirmed defects observed

Record the `TM-DEF-*` ID, pytest node ID and sanitized evidence path.

## Unexpected failures

Record the first causal failure, classification and next action. Do not classify an automation or environment failure as a product defect without evidence.

## Coverage gaps

See `docs/test-plan.md`. Record any additional unverified behavior discovered during this run.
