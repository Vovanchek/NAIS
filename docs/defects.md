# Defects Found

All findings below were reproduced against `https://test-me.vzl.one/`. Assertions retain the stated requirements; observed behavior is not used as the expected result.

## TM-DEF-001: Coupon is not case-insensitive

- **Severity / priority:** High / P0
- **Environment:** Published API, seed `test-me-v3`, observed 2026-10-20.
- **Preconditions:** Create a new workspace; select any in-stock product using `GET /api/products`.
- **Steps:** POST `/api/quote` with `{"items":[{"product_id":"p01","quantity":1}],"coupon":"welcome10","delivery":"standard"}` and `X-Workspace-Token`.
- **Expected:** Coupon matching is case-insensitive; valid quote with 10% item discount.
- **Actual:** HTTP 422, `{"detail":"Невідомий промокод"}`. Exact uppercase `WELCOME10` is accepted. The padded uppercase variant was also run as part of the regression test.
- **Evidence:** [Selenium MCP screenshot](evidence/DEF-001-coupon-case.png); API regression `tests/api/test_quote.py::test_welcome_coupon_is_case_and_whitespace_insensitive`; reproduced again in `pytest tests/api/test_quote.py` (6 passed, 2 failed).
- **Reproducibility:** Reproduced on separate fresh workspaces.
- **Affected test:** `test_welcome_coupon_is_case_and_whitespace_insensitive`.
- **GitHub Issue:** Bug #4; primary test case #14.
- **Automation:** `tests/api/test_quote.py::test_welcome_coupon_is_case_and_whitespace_insensitive`; marker `known_defect`; `xfail(strict=True)`.

## TM-DEF-002: Free-shipping threshold is not inclusive

- **Severity / priority:** High / P0
- **Environment:** Published API, seed `test-me-v3`, observed 2026-10-20.
- **Preconditions:** Create a new workspace; use live product `p02`, whose API price is 150000 kopecks.
- **Steps:** POST `/api/quote` with one `p02`, quantity 1, empty coupon, standard delivery.
- **Expected:** Standard shipping is free from 150000 kopecks inclusive.
- **Actual:** Quote returns `shipping=8000`, `total=158000`, `currency=UAH` at exactly 150000. The UI itself labels standard shipping free from 1500 UAH.
- **Evidence:** [Selenium MCP screenshot](evidence/DEF-002-shipping-threshold.png); API regression `tests/api/test_quote.py::test_standard_shipping_threshold_is_inclusive`; quote suite failure `expected 0, got 8000`.
- **Reproducibility:** Reproduced with the live seed product at the exact boundary.
- **Affected test:** `test_standard_shipping_threshold_is_inclusive`.
- **GitHub Issue:** Bug #1; primary test case #12.
- **Automation:** `tests/api/test_quote.py::test_standard_shipping_threshold_is_inclusive`; marker `known_defect`; `xfail(strict=True)`.

## TM-DEF-003: Repeated order cancellation succeeds instead of conflicting

- **Severity / priority:** Medium / P0
- **Environment:** Published API, observed 2026-10-20.
- **Preconditions:** New workspace; create an approved order with live in-stock product and synthetic contact data.
- **Steps:** POST `/api/orders/{id}/cancel` twice with the same workspace token.
- **Expected:** First request returns 200 and `cancelled`; second returns 409.
- **Actual:** Both requests return HTTP 200 and `{"id":"<order-id>","status":"cancelled"}`.
- **Evidence:** [Selenium MCP screenshot](evidence/DEF-003-repeat-cancel.png) shows the cancelled order. Selenium MCP WebDriver BiDi captured two `POST /api/orders/{id}/cancel` responses, both HTTP 200; the second body was `{"id":"<order-id>","status":"cancelled"}`. API regression: `tests/api/test_orders.py::test_repeated_order_cancellation_returns_conflict`.
- **Reproducibility:** Reproduced on two separately created orders.
- **Affected test:** `test_repeated_order_cancellation_returns_conflict`.
- **GitHub Issue:** Bug #2; primary test case #40.
- **Automation:** `tests/api/test_orders.py::test_repeated_order_cancellation_returns_conflict`; marker `known_defect`; `xfail(strict=True)`.

## TM-DEF-004: Catalog search is case-sensitive

- **Severity / priority:** Medium / P1
- **Environment:** Published API, seed `test-me-v3`, observed 2026-10-20.
- **Preconditions:** New workspace; product `p01` is returned by `GET /api/products` with name `Бездротові навушники «Орбіта»`.
- **Steps:** GET `/api/products?q=бЕЗД&limit=20`.
- **Expected:** Case-insensitive search returns `p01`.
- **Actual:** HTTP 200 with no matching product; the same query in original case returns `p01`.
- **Evidence:** [Selenium MCP screenshot](evidence/DEF-004-case-sensitive-search.png) shows query `бЕЗД` and zero results; API regression `tests/api/test_catalog.py::test_search_is_case_insensitive_and_trims_query` reports the mixed-case variant specifically.
- **Reproducibility:** Reproduced using the live seed product.
- **Affected test:** `test_search_is_case_insensitive_and_trims_query`.
- **GitHub Issue:** Bug #3; primary test case #27.
- **Automation:** `tests/api/test_catalog.py::test_search_is_case_insensitive_and_trims_query`; marker `known_defect`; `xfail(strict=True)`.

## Verification notes

No server-side implementation was available or changed. These are application defects inferred only from repeatable HTTP/UI observations. Failure artifact paths apply to UI failures; API evidence is the named pytest case and its assertion output.
