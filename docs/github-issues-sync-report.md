# GitHub Issues Sync Report

## Summary

- Issues before changes: 26 (25 open, 1 closed).
- Issues after changes: 41 (39 open, 2 closed).
- Primary test cases: 35.
- Duplicate Issues: 2 (#22 and #25).
- Bug Issues: 4 (#1-#4; all remain open).
- Known-defect tests: 4.
- Business pytest tests: 35.
- Traceability coverage: 100% (35/35 business tests have one primary test-case ID, one GitHub Issue, and one exact collected pytest node ID).

## Updated Issues

| Issue | Changes | Test case / defect ID | Exact pytest node ID | Labels applied | Final state |
|---:|---|---|---|---|---|
| #1 | Added defect ID and automation metadata; retained open bug | `TM-DEF-002` | `tests/api/test_quote.py::test_standard_shipping_threshold_is_inclusive` | `bug`, `api`, `priority:P0`, `known-defect` | OPEN |
| #2 | Replaced stale lifecycle reference with repeated-cancellation test metadata | `TM-DEF-003` | `tests/api/test_orders.py::test_repeated_order_cancellation_returns_conflict` | `bug`, `api`, `priority:P0`, `known-defect` | OPEN |
| #3 | Added defect ID and automation metadata | `TM-DEF-004` | `tests/api/test_catalog.py::test_search_is_case_insensitive_and_trims_query` | `bug`, `api`, `priority:P1`, `known-defect` | OPEN |
| #4 | Added defect ID and automation metadata | `TM-DEF-001` | `tests/api/test_quote.py::test_welcome_coupon_is_case_and_whitespace_insensitive` | `bug`, `api`, `priority:P0`, `known-defect` | OPEN |
| #5 | Corrected case ID and exact behavior mapping | `TM-API-AUTH-001` | `tests/api/test_authorization.py::test_stateful_endpoints_reject_missing_and_invalid_tokens` | `test-case`, `automated`, `api`, `negative`, `priority:P0` | OPEN |
| #6 | Corrected case ID and exact behavior mapping | `TM-API-AUTH-002` | `tests/api/test_smoke.py::test_protected_orders_reject_missing_and_invalid_workspace_tokens` | `test-case`, `automated`, `api`, `negative`, `priority:P0` | OPEN |
| #7 | Corrected case ID to match catalog list/detail smoke test | `TM-API-CATALOG-009` | `tests/api/test_smoke.py::test_catalog_lists_products_and_product_detail` | `test-case`, `automated`, `api`, `smoke`, `priority:P0` | OPEN |
| #8 | Corrected case ID to the traceability matrix | `TM-API-SMOKE-001` | `tests/api/test_smoke.py::test_health_endpoint_reports_service_status` | `test-case`, `automated`, `api`, `smoke`, `priority:P0` | OPEN |
| #9 | Applied consistent test-case automation labels | `TM-API-WORKSPACE-001` | `tests/api/test_smoke.py::test_create_workspace_returns_token_without_authorization` | `test-case`, `automated`, `api`, `smoke`, `priority:P0` | OPEN |
| #10 | Narrowed former aggregated quote case to valid quantity boundaries | `TM-API-QUOTE-005` | `tests/api/test_quote.py::test_valid_quantity_boundaries_are_quoted` | `test-case`, `automated`, `api`, `regression`, `priority:P0` | OPEN |
| #11 | Applied consistent test-case automation labels | `TM-API-QUOTE-004` | `tests/api/test_quote.py::test_delivery_charge_is_not_discounted` | `test-case`, `automated`, `api`, `regression`, `priority:P0` | OPEN |
| #12 | Narrowed to shipping threshold behavior; added known-defect metadata | `TM-API-QUOTE-003` / `TM-DEF-002` | `tests/api/test_quote.py::test_standard_shipping_threshold_is_inclusive` | `test-case`, `automated`, `api`, `regression`, `known-defect`, `priority:P0` | OPEN |
| #13 | Applied consistent test-case automation labels | `TM-API-QUOTE-002` | `tests/api/test_quote.py::test_unknown_coupon_is_rejected` | `test-case`, `automated`, `api`, `negative`, `priority:P0` | OPEN |
| #14 | Added known-defect ID, marker, strict-xfail, and exact-node metadata | `TM-API-QUOTE-001` / `TM-DEF-001` | `tests/api/test_quote.py::test_welcome_coupon_is_case_and_whitespace_insensitive` | `test-case`, `automated`, `api`, `regression`, `known-defect`, `priority:P0` | OPEN |
| #15 | Narrowed former aggregated review case to valid review boundaries | `TM-API-REVIEW-001` | `tests/api/test_workspace_reviews_favorites.py::test_review_accepts_rating_and_text_length_boundaries` | `test-case`, `automated`, `api`, `regression`, `priority:P1` | OPEN |
| #16 | Narrowed former catalog aggregate to category filtering | `TM-API-CATALOG-001` | `tests/api/test_catalog.py::test_category_filter_returns_only_requested_category` | `test-case`, `automated`, `api`, `regression`, `priority:P1` | OPEN |
| #17 | Corrected case ID to `TM-API-ORDER-004` | `TM-API-ORDER-004` | `tests/api/test_orders.py::test_order_is_not_visible_from_another_workspace` | `test-case`, `automated`, `api`, `negative`, `priority:P1` | OPEN |
| #18 | Corrected case ID to `TM-API-ORDER-003` | `TM-API-ORDER-003` | `tests/api/test_orders.py::test_declined_payment_does_not_create_order` | `test-case`, `automated`, `api`, `negative`, `priority:P0` | OPEN |
| #19 | Removed repeated cancellation from scope and expected result; retained first cancellation only | `TM-API-ORDER-001` | `tests/api/test_orders.py::test_approved_order_lifecycle_and_repeat_cancel_conflict` | `test-case`, `automated`, `api`, `regression`, `priority:P0` | OPEN |
| #20 | Narrowed former aggregated review case to duplicate review behavior | `TM-API-REVIEW-004` | `tests/api/test_workspace_reviews_favorites.py::test_duplicate_review_returns_409` | `test-case`, `automated`, `api`, `regression`, `priority:P1` | OPEN |
| #21 | Applied consistent UI smoke/regression labels | `TM-UI-CHECKOUT-001` | `tests/ui/test_checkout.py::test_checkout_applies_coupon_persists_order_and_clears_cart` | `test-case`, `automated`, `ui`, `smoke`, `regression`, `priority:P0` | OPEN |
| #22 | Added required duplicate comment and `duplicate` label; retained closed state | Duplicate of #21; not primary coverage | `tests/ui/test_checkout.py::test_checkout_applies_coupon_persists_order_and_clears_cart` | `duplicate` | CLOSED |
| #23 | Applied consistent UI automation labels | `TM-UI-CHECKOUT-002` | `tests/ui/test_checkout.py::test_double_submit_guard_creates_only_one_order` | `test-case`, `automated`, `ui`, `regression`, `priority:P1` | OPEN |
| #24 | Replaced hardcoded `p01` data with dynamic live-catalog selection; updated steps and labels | `TM-UI-FAVORITES-001` | `tests/ui/test_favorites.py::test_favorite_toggle_persists_after_reload` | `test-case`, `automated`, `ui`, `regression`, `priority:P1` | OPEN |
| #25 | Added required duplicate comment and `duplicate` label; retained closed state | Duplicate of #24; not primary coverage | `tests/ui/test_favorites.py::test_favorite_toggle_persists_after_reload` | `duplicate` | CLOSED |
| #26 | Applied consistent API automation labels | `TM-API-FAVORITES-001` | `tests/api/test_workspace_reviews_favorites.py::test_favorites_persist_and_are_isolated` | `test-case`, `automated`, `api`, `regression`, `priority:P1` | OPEN |

## Created Issues

| Issue | Test case ID | Exact pytest node ID | Labels | Final state |
|---:|---|---|---|---|
| #27 | `TM-API-CATALOG-002` | `tests/api/test_catalog.py::test_search_is_case_insensitive_and_trims_query` | `test-case`, `automated`, `api`, `regression`, `known-defect`, `priority:P1` | OPEN |
| #28 | `TM-API-CATALOG-003` | `tests/api/test_catalog.py::test_in_stock_filter_excludes_zero_stock_products` | `test-case`, `automated`, `api`, `regression`, `priority:P1` | OPEN |
| #29 | `TM-API-CATALOG-004` | `tests/api/test_catalog.py::test_price_bounds_are_inclusive` | `test-case`, `automated`, `api`, `regression`, `priority:P1` | OPEN |
| #30 | `TM-API-CATALOG-005` | `tests/api/test_catalog.py::test_min_price_greater_than_max_price_returns_422` | `test-case`, `automated`, `api`, `negative`, `priority:P1` | OPEN |
| #31 | `TM-API-CATALOG-006` | `tests/api/test_catalog.py::test_price_sort_is_numeric` | `test-case`, `automated`, `api`, `regression`, `priority:P1` | OPEN |
| #32 | `TM-API-CATALOG-007` | `tests/api/test_catalog.py::test_pagination_and_limit_boundaries` | `test-case`, `automated`, `api`, `regression`, `priority:P1` | OPEN |
| #33 | `TM-API-CATALOG-008` | `tests/api/test_catalog.py::test_combined_catalog_filters` | `test-case`, `automated`, `api`, `regression`, `priority:P1` | OPEN |
| #34 | `TM-API-QUOTE-006` | `tests/api/test_quote.py::test_quantity_outside_schema_bounds_returns_422` | `test-case`, `automated`, `api`, `negative`, `priority:P0` | OPEN |
| #35 | `TM-API-QUOTE-007` | `tests/api/test_quote.py::test_stock_shortage_returns_409` | `test-case`, `automated`, `api`, `negative`, `priority:P0` | OPEN |
| #36 | `TM-API-QUOTE-008` | `tests/api/test_quote.py::test_out_of_stock_product_cannot_be_quoted` | `test-case`, `automated`, `api`, `negative`, `priority:P0` | OPEN |
| #37 | `TM-API-REVIEW-002` | `tests/api/test_workspace_reviews_favorites.py::test_invalid_review_rating_returns_422` | `test-case`, `automated`, `api`, `negative`, `priority:P1` | OPEN |
| #38 | `TM-API-REVIEW-003` | `tests/api/test_workspace_reviews_favorites.py::test_review_text_length_outside_bounds_returns_422` | `test-case`, `automated`, `api`, `negative`, `priority:P1` | OPEN |
| #39 | `TM-API-REVIEW-005` | `tests/api/test_workspace_reviews_favorites.py::test_review_is_not_visible_in_another_workspace` | `test-case`, `automated`, `api`, `regression`, `priority:P1` | OPEN |
| #40 | `TM-API-ORDER-002` | `tests/api/test_orders.py::test_repeated_order_cancellation_returns_conflict` | `test-case`, `automated`, `api`, `negative`, `regression`, `known-defect`, `priority:P0` | OPEN |
| #41 | `TM-UI-CHECKOUT-003` | `tests/ui/test_checkout.py::test_declined_payment_keeps_cart_and_does_not_create_order` | `test-case`, `automated`, `ui`, `negative`, `regression`, `priority:P0` | OPEN |

## Duplicate Issues

- Primary #21; duplicate #22. #22 is closed, has label `duplicate`, and contains the requested comment.
- Primary #24; duplicate #25. #25 is closed, has label `duplicate`, and contains the requested comment.

## Labels

Created: `test-case`, `automated`, `api`, `ui`, `smoke`, `regression`, `negative`, `priority:P0`, `priority:P1`, `known-defect`, and `qa-tracking`.

The existing `duplicate` label was applied to #22 and #25. Labels were applied to test-case and bug Issues according to surface, priority, automation, regression/negative, and known-defect status. `qa-tracking` was created as required; no umbrella Issue was needed because each former aggregate was narrowed to one primary behavior.

## Validation

| Command | Result |
|---|---|
| `python -m pytest --collect-only -q` (before changes) | 42 tests collected |
| `python -m pytest tests/unit -q` (before changes) | 7 passed |
| `python -m ruff format --check .` (before changes) | 29 files already formatted |
| `python -m ruff check .` (before changes) | All checks passed |
| `python -m ruff format --check .` (after changes) | 29 files already formatted |
| `python -m ruff check .` (after changes) | All checks passed |
| `python -m pytest --collect-only -q` (after changes) | 42 tests collected: 35 business tests and 7 framework unit tests |
| `python -m pytest tests/unit -q` (after changes) | 7 passed |
| `python -m pytest -m "api and not known_defect" -q` | 27 passed, 15 deselected |
| `python -m pytest -m known_defect -rxX` | 4 expected xfails; 38 deselected |
| Final GitHub/docs matrix audit | 41 Issues; 35 unique primary IDs and nodes; all 35 collected business nodes mapped; duplicate, defect, label, and state checks passed |
| `git diff --check` | Passed |

The UI suite was not run because no UI code changed; collection confirmed its exact node IDs.

## Remaining gaps

No business-test traceability gaps remain. Four confirmed product defects (`TM-DEF-001` through `TM-DEF-004`) remain unfixed and their bug Issues remain open by policy. Their strict known-defect tests were run and xfailed as expected.
