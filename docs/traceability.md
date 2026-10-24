# Automation Traceability Matrix

Every business-facing automated test maps one-to-one to a stable test case ID and one primary GitHub Issue. Exact node IDs below were collected with `python -m pytest --collect-only -q`. Confirmed product defects remain linked from their separate bug Issues and retain strict expected-failure checks.

| Test case ID | Requirement / behavior | Priority | Type | GitHub Issue | Exact pytest node ID | Automation status | Known defect ID |
|---|---|---:|---|---:|---|---|---|
| `TM-API-AUTH-001` | Reject missing/invalid tokens on stateful endpoints | P0 | API negative | #5 | `tests/api/test_authorization.py::test_stateful_endpoints_reject_missing_and_invalid_tokens` | Automated | — |
| `TM-API-CATALOG-001` | Category filter | P1 | API regression | #16 | `tests/api/test_catalog.py::test_category_filter_returns_only_requested_category` | Automated | — |
| `TM-API-CATALOG-002` | Case-insensitive, whitespace-trimmed search | P1 | API regression | #27 | `tests/api/test_catalog.py::test_search_is_case_insensitive_and_trims_query` | Known defect; `known_defect`; `xfail(strict=True)` | `TM-DEF-004` |
| `TM-API-CATALOG-003` | In-stock filter excludes zero-stock products | P1 | API regression | #28 | `tests/api/test_catalog.py::test_in_stock_filter_excludes_zero_stock_products` | Automated | — |
| `TM-API-CATALOG-004` | Inclusive price bounds | P1 | API regression | #29 | `tests/api/test_catalog.py::test_price_bounds_are_inclusive` | Automated | — |
| `TM-API-CATALOG-005` | Invalid price range returns HTTP 422 | P1 | API negative | #30 | `tests/api/test_catalog.py::test_min_price_greater_than_max_price_returns_422` | Automated | — |
| `TM-API-CATALOG-006` | Numeric price sort | P1 | API regression | #31 | `tests/api/test_catalog.py::test_price_sort_is_numeric` | Automated | — |
| `TM-API-CATALOG-007` | Pagination and limit boundaries | P1 | API regression | #32 | `tests/api/test_catalog.py::test_pagination_and_limit_boundaries` | Automated | — |
| `TM-API-CATALOG-008` | Combined catalog filters | P1 | API regression | #33 | `tests/api/test_catalog.py::test_combined_catalog_filters` | Automated | — |
| `TM-API-ORDER-001` | Approved order lifecycle and first cancellation | P0 | API regression | #19 | `tests/api/test_orders.py::test_approved_order_lifecycle_and_repeat_cancel_conflict` | Automated | — |
| `TM-API-ORDER-002` | Repeated cancellation returns conflict | P0 | API negative regression | #40 | `tests/api/test_orders.py::test_repeated_order_cancellation_returns_conflict` | Known defect; `known_defect`; `xfail(strict=True)` | `TM-DEF-003` |
| `TM-API-ORDER-003` | Declined payment has no order/stock side effects | P0 | API negative | #18 | `tests/api/test_orders.py::test_declined_payment_does_not_create_order` | Automated | — |
| `TM-API-ORDER-004` | Order isolation across workspaces | P1 | API negative | #17 | `tests/api/test_orders.py::test_order_is_not_visible_from_another_workspace` | Automated | — |
| `TM-API-QUOTE-001` | Coupon normalization and totals | P0 | API regression | #14 | `tests/api/test_quote.py::test_welcome_coupon_is_case_and_whitespace_insensitive` | Known defect; `known_defect`; `xfail(strict=True)` | `TM-DEF-001` |
| `TM-API-QUOTE-002` | Unknown coupon rejected | P0 | API negative | #13 | `tests/api/test_quote.py::test_unknown_coupon_is_rejected` | Automated | — |
| `TM-API-QUOTE-003` | Inclusive free-shipping threshold | P0 | API regression | #12 | `tests/api/test_quote.py::test_standard_shipping_threshold_is_inclusive` | Known defect; `known_defect`; `xfail(strict=True)` | `TM-DEF-002` |
| `TM-API-QUOTE-004` | Delivery charge is not discounted | P0 | API regression | #11 | `tests/api/test_quote.py::test_delivery_charge_is_not_discounted` | Automated | — |
| `TM-API-QUOTE-005` | Valid quantity boundaries | P0 | API regression | #10 | `tests/api/test_quote.py::test_valid_quantity_boundaries_are_quoted` | Automated | — |
| `TM-API-QUOTE-006` | Invalid quantity schema bounds | P0 | API negative | #34 | `tests/api/test_quote.py::test_quantity_outside_schema_bounds_returns_422` | Automated | — |
| `TM-API-QUOTE-007` | Stock shortage | P0 | API negative | #35 | `tests/api/test_quote.py::test_stock_shortage_returns_409` | Automated | — |
| `TM-API-QUOTE-008` | Out-of-stock product quote | P0 | API negative | #36 | `tests/api/test_quote.py::test_out_of_stock_product_cannot_be_quoted` | Automated | — |
| `TM-API-SMOKE-001` | Health endpoint | P0 | API smoke | #8 | `tests/api/test_smoke.py::test_health_endpoint_reports_service_status` | Automated | — |
| `TM-API-WORKSPACE-001` | Workspace creation | P0 | API smoke | #9 | `tests/api/test_smoke.py::test_create_workspace_returns_token_without_authorization` | Automated | — |
| `TM-API-CATALOG-009` | Catalog list and product detail | P0 | API smoke | #7 | `tests/api/test_smoke.py::test_catalog_lists_products_and_product_detail` | Automated | — |
| `TM-API-AUTH-002` | Orders reject missing/invalid tokens | P0 | API negative | #6 | `tests/api/test_smoke.py::test_protected_orders_reject_missing_and_invalid_workspace_tokens` | Automated | — |
| `TM-API-FAVORITES-001` | Favorites persistence and workspace isolation | P1 | API regression | #26 | `tests/api/test_workspace_reviews_favorites.py::test_favorites_persist_and_are_isolated` | Automated | — |
| `TM-API-REVIEW-001` | Valid review boundaries | P1 | API regression | #15 | `tests/api/test_workspace_reviews_favorites.py::test_review_accepts_rating_and_text_length_boundaries` | Automated | — |
| `TM-API-REVIEW-002` | Invalid rating | P1 | API negative | #37 | `tests/api/test_workspace_reviews_favorites.py::test_invalid_review_rating_returns_422` | Automated | — |
| `TM-API-REVIEW-003` | Invalid review text length | P1 | API negative | #38 | `tests/api/test_workspace_reviews_favorites.py::test_review_text_length_outside_bounds_returns_422` | Automated | — |
| `TM-API-REVIEW-004` | Duplicate review | P1 | API regression | #20 | `tests/api/test_workspace_reviews_favorites.py::test_duplicate_review_returns_409` | Automated | — |
| `TM-API-REVIEW-005` | Review isolation across workspaces | P1 | API regression | #39 | `tests/api/test_workspace_reviews_favorites.py::test_review_is_not_visible_in_another_workspace` | Automated | — |
| `TM-UI-CHECKOUT-001` | Approved checkout, persistence, and cart clear | P0 | UI smoke regression | #21 | `tests/ui/test_checkout.py::test_checkout_applies_coupon_persists_order_and_clears_cart` | Automated | — |
| `TM-UI-CHECKOUT-002` | Double-submit protection | P1 | UI regression | #23 | `tests/ui/test_checkout.py::test_double_submit_guard_creates_only_one_order` | Automated | — |
| `TM-UI-CHECKOUT-003` | Declined payment retains cart and creates no order | P0 | UI negative regression | #41 | `tests/ui/test_checkout.py::test_declined_payment_keeps_cart_and_does_not_create_order` | Automated | — |
| `TM-UI-CHECKOUT-004` | Approved checkout with express delivery, expected total, and reload persistence | P0 | UI regression | #45 | `tests/ui/test_checkout_additional_e2e.py::test_checkout_express_delivery_creates_confirmed_order` | Automated | — |
| `TM-UI-CHECKOUT-005` | Invalid tampered payment value shows error, creates no order, and keeps cart items | P0 | UI negative regression | #46 | `tests/ui/test_checkout_additional_e2e.py::test_checkout_rejects_invalid_payment_value_without_creating_order` | Automated | — |
| `TM-UI-FAVORITES-001` | Favorite toggle and reload persistence | P1 | UI regression | #24 | `tests/ui/test_favorites.py::test_favorite_toggle_persists_after_reload` | Automated | — |

## Known-defect links

| Defect ID | Bug Issue | Test-case Issue | Exact pytest node ID | Marker / expectation |
|---|---:|---:|---|---|
| `TM-DEF-001` | #4 | #14 | `tests/api/test_quote.py::test_welcome_coupon_is_case_and_whitespace_insensitive` | `known_defect`; `xfail(strict=True)` |
| `TM-DEF-002` | #1 | #12 | `tests/api/test_quote.py::test_standard_shipping_threshold_is_inclusive` | `known_defect`; `xfail(strict=True)` |
| `TM-DEF-003` | #2 | #40 | `tests/api/test_orders.py::test_repeated_order_cancellation_returns_conflict` | `known_defect`; `xfail(strict=True)` |
| `TM-DEF-004` | #3 | #27 | `tests/api/test_catalog.py::test_search_is_case_insensitive_and_trims_query` | `known_defect`; `xfail(strict=True)` |

## Framework self-tests

Framework self-tests validate token redaction, UAH parsing, integer rounding, host safety, rate-limit diagnostics, artifact-path sanitization, and exception-safe artifact capture. These tests are infrastructure checks and do not receive business-facing test-case Issues.

```bash
python -m pytest tests/unit -q
```

## Maintenance rule

Any pull request that adds, renames, or removes a business test must update this matrix and [`test-cases.md`](test-cases.md), including its primary GitHub Issue. Confirmed defects must use the matching `TM-DEF-*` ID, the `known_defect` marker, and `xfail(strict=True)`; defect Issues remain open until the product behavior is fixed and verified.
