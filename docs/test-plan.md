# Test Plan

## Objective

Validate the published Test Me storefront at `https://test-me.vzl.one/` through its OpenAPI-documented API and its public UI. Prioritize independent, reproducible workspace-isolated tests for pricing, checkout, and order lifecycle. Assertions represent the stated contract even when the current application violates it.

## Scope and priorities

- **P0:** API health/workspace/catalog foundation; authorization; quote arithmetic, coupons, delivery and stock; approved/declined order lifecycle; one Selenium checkout E2E including persistence and cart clearing.
- **P1:** catalog filters/search/sort/pagination; workspace isolation; review validation/persistence; favorites API/UI persistence; UI double-submit guard.
- **P2:** comparison, cart quantity/removal/promo persistence, order search/filter/reorder, reset, mobile/theme/accessibility, controlled network failures, broader browser coverage, and parallel stability.

## Environment

- UI and API: `https://test-me.vzl.one/`
- OpenAPI source: `https://test-me.vzl.one/openapi.json`
- Python 3.11+, pytest, requests, Selenium 4, Chrome by default; Selenium Manager resolves the driver.
- The published seed dataset is read at runtime. Product IDs/prices/stock used in boundaries are selected from live API data, except stable review IDs where the API validates the identified seed product.
- Workspace tokens are created per API test and never printed. UI tokens are read only inside the UI test process and are not included in artifacts.

## Strategy

- API tests cover more combinations because they can deterministically inspect currency-unit values, boundary validation, response statuses, persistence, and workspace isolation.
- UI focuses on critical user journeys and stable published `data-testid`/semantic selectors; browser mechanics stay in Page Objects.
- All money math uses integer kopiykas. Contacts are synthetic (`QA Synthetic`, `qa.synthetic@example.com`, `Test Address 1`); no payment is processed.
- Write requests are limited; tests use one function-scoped workspace each, with related variants grouped inside a test. Do not run high worker counts against the 30-workspaces/minute limit.

## Entry and exit criteria

- Entry: approved network access to the stated host, Python dependencies installed, and Chrome available.
- Exit: Ruff formatter/lint and pytest collection pass; API and UI suites have been run; failures have actual evidence and are classified as application defects or environment limitations.
- A red regression test for a reproducible contract violation is an expected test result, not a passing application result.

## Known limitations and out of scope

- Current seed prices are all divisible by 10 kopecks. Public quote data therefore cannot exercise a subtotal whose 10% discount has a fractional kopeck; the floor formula is asserted where representable, but the rounding edge remains unverified.
- No server-side access is available. API response schemas are sparse in OpenAPI, so response shapes are asserted only after observation from the published service.
- P2 comparisons, order filtering/reorder, reset workflow, 360px viewport, theme, keyboard/accessibility scans, controlled outage, cross-browser, and parallel runs are not implemented in this timebox.
- No tests run against any domain other than the specified host. No real personal/payment data, repository tokens, or cookies are used.

## Timebox rationale

The implementation prioritizes live-contract discovery, API financial/lifecycle coverage, and one critical UI checkout over broad surface-level tests. Further UI expansion should follow stabilization of the four defects recorded in `defects.md`.

## Approximate time allocation

- 15–20 minutes: OpenAPI and live UI discovery.
- 25–35 minutes: framework configuration, API client, fixtures, and artifacts.
- 40–50 minutes: API P0 smoke, quote, and order lifecycle.
- 35–45 minutes: UI checkout E2E and double-submit guard.
- 20–30 minutes: P1 catalog/isolation/review/favorites and documentation.
- 15–20 minutes: lint, collection, suite reruns, and final review.
