# Test Me Automation

Risk-prioritized UI and API automation for the published training shop at `https://test-me.vzl.one/`. The suite uses Python, Selenium 4, pytest, requests, Page Objects, isolated API workspaces, and integer-kopeck assertions. The OpenAPI source is `https://test-me.vzl.one/openapi.json`.

## Requirements

- Python 3.11 or newer
- Google Chrome (default), Firefox, or Edge
- Node.js/npm only if using the optional Selenium MCP integration in VS Code

Selenium Manager resolves browser drivers automatically. Tests use synthetic contact values; no real payment is performed.

## Setup

PowerShell, without activating the environment (works when script execution is restricted):

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

If PowerShell permits activation, the equivalent is:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Configuration

`BASE_URL` defaults to the permitted host and rejects other hosts. It may only be overridden to `https://test-me.vzl.one`. Other settings:

| Variable | Default | Purpose |
|---|---|---|
| `BROWSER` | `chrome` | `chrome`, `firefox`, or `edge` |
| `HEADLESS` | `true` | Run headless when true |
| `API_CONNECT_TIMEOUT` | `5` | HTTP connection timeout in seconds |
| `API_READ_TIMEOUT` | `20` | HTTP response timeout in seconds |
| `ARTIFACT_DIR` | `artifacts` | UI failure evidence directory |

## Run

```powershell
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m pytest --collect-only -q
.\.venv\Scripts\python.exe -m pytest -m api -q
.\.venv\Scripts\python.exe -m pytest -m "ui and smoke" -q
.\.venv\Scripts\python.exe -m pytest tests\api -q
.\.venv\Scripts\python.exe -m pytest tests\ui -q
```

For a visible Firefox run:

```powershell
$env:BROWSER = "firefox"
$env:HEADLESS = "false"
.\.venv\Scripts\python.exe -m pytest -m ui -q
```

Optional API parallel run uses separate function-scoped workspaces; keep workers low because the service allows at most 30 workspace creations per minute:

```powershell
.\.venv\Scripts\python.exe -m pytest -m api -n 2
```

## Artifacts and defects

On UI failure the fixture saves `screenshot.png`, `page_source.html`, and `failure.txt` under the ignored `artifacts/` directory. Workspace tokens are masked/redacted. Current reproducible findings and evidence references are in [`docs/defects.md`](docs/defects.md); planned and covered scenarios are in [`docs/test-plan.md`](docs/test-plan.md) and [`docs/test-cases.md`](docs/test-cases.md).

The current suite intentionally has regression failures for confirmed application defects. See `Known defects` in `docs/defects.md`; expected assertions have not been weakened to match the broken behavior.

## MCP browser discovery

The VS Code Selenium MCP server is configured in `.vscode/mcp.json`. Start it from the MCP Servers view to inspect the live page, confirm locators, and observe browser/network diagnostics. Network diagnostics may not expose full response bodies; use the API client/tests to verify response contracts.

## Publish to GitHub

Create an empty repository in your GitHub account, then run in PowerShell from the project directory:

```powershell
git init
git add .
git commit -m "Add Test Me automation framework"
git branch -M main
git remote add origin "https://github.com/YOUR-USER/YOUR-REPOSITORY.git"
git push -u origin main
```

Review `git status` and ensure no `.venv`, artifacts, tokens, cookies, or real personal data are staged before pushing. The repository has not been published on the user's behalf.
