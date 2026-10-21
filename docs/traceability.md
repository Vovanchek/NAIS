# Automation Traceability Matrix

Every business-facing automated test has a stable case ID and an exact pytest node ID. Framework unit tests are tracked separately.

| Test case ID | Priority | Requirement / behavior | Pytest node ID | Status |
|---|---:|---|---|---|
| `TM-API-AUTH-001` | P0 | Authorization | `tests/api/test_authorization.py::test_stateful_endpoints_reject_missing_and_invalid_tokens` | Automated |
| `TM-API-CATALOG-001` | P1 | Category filter | `tests/api/test_catalog.py::test_category_filter_returns_only_requested_category` | Automated |
| `TM-API-CATALOG-002` | P1 | Search normalization | `tests/api/test_catalog.py::test_search_is_case_insensitive_and_trims_query` | Known defect TM-DEF-004 |
| `TM-API-CATALOG-003` | P1 | In-stock filter | `tests/api/test_catalog.py::test_in_stock_filter_excludes_zero_stock_products` | Automated |
| `TM-API-CATALOG-004` | P1 | Inclusive price bounds | `tests/api/test_catalog.py::test_price_bounds_are_inclusive` | Automated |
| `TM-API-CATALOG-005` | P1 | Invalid price range | `tests/api/test_catalog.py::test_min_price_greater_than_max_price_returns_422` | Automated |
| `TM-API-CATALOG-006` | P1 | Numeric price sorting | `tests/api/test_catalog.py::test_price_sort_is_numeric` | Automated |
| `TM-API-CATALOG-007` | P1 | Pagination and limit boundaries | `tests/api/test_catalog.py::test_pagination_and_limit_boundaries` | Automated |
| `TM-API-CATALOG-008` | P1 | Combined filters | `tests/api/test_catalog.py::test_combined_catalog_filters` | Automated |
| `TM-API-ORDER-001` | P0 | Approved lifecycle and first cancellation | `tests/api/test_orders.py::test_approved_order_lifecycle_and_repeat_cancel_conflict` | Automated |
| `TM-API-ORDER-002` | P0 | Repeated cancellation conflict | `tests/api/test_orders.py::test_repeated_order_cancellation_returns_conflict` | Known defect TM-DEF-003 |
| `TM-API-ORDER-003` | P0 | Declined payment | `tests/api/test_orders.py::test_declined_payment_does_not_create_order` | Automated |
| `TM-API-ORDER-004` | P1 | Workspace order isolation | `tests/api/test_orders.py::test_order_is_not_visible_from_another_workspace` | Automated |
| `TM-API-QUOTE-001` | P0 | Coupon normalization and totals | `tests/api/test_quote.py::test_welcome_coupon_is_case_and_whitespace_insensitive` | Known defect TM-DEF-001 |
| `TM-API-QUOTE-002` | P0 | Unknown coupon | `tests/api/test_quote.py::test_unknown_coupon_is_rejected` | Automated |
| `TM-API-QUOTE-003` | P0 | Inclusive free-shipping threshold | `tests/api/test_quote.py::test_standard_shipping_threshold_is_inclusive` | Known defect TM-DEF-002 |
| `TM-API-QUOTE-004` | P0 | Delivery is not discounted | `tests/api/test_quote.py::test_delivery_charge_is_not_discounted` | Automated |
| `TM-API-QUOTE-005` | P0 | Valid quantity boundaries | `tests/api/test_quote.py::test_valid_quantity_boundaries_are_quoted` | Automated |
| `TM-API-QUOTE-006` | P0 | Invalid quantity schema bounds | `tests/api/test_quote.py::test_quantity_outside_schema_bounds_returns_422` | Automated |
| `TM-API-QUOTE-007` | P0 | Stock shortage | `tests/api/test_quote.py::test_stock_shortage_returns_409` | Automated |
| `TM-API-QUOTE-008` | P0 | Out-of-stock product | `tests/api/test_quote.py::test_out_of_stock_product_cannot_be_quoted` | Automated |
| `TM-API-SMOKE-001` | P0 | Health | `tests/api/test_smoke.py::test_health_endpoint_reports_service_status` | Automated |
| `TM-API-WORKSPACE-001` | P0 | Workspace creation | `tests/api/test_smoke.py::test_create_workspace_returns_token_without_authorization` | Automated |
| `TM-API-CATALOG-009` | P0 | Catalog list and detail | `tests/api/test_smoke.py::test_catalog_lists_products_and_product_detail` | Automated |
| `TM-API-AUTH-002` | P0 | Orders reject missing/invalid token | `tests/api/test_smoke.py::test_protected_orders_reject_missing_and_invalid_workspace_tokens` | Automated |
| `TM-API-FAVORITES-001` | P1 | Favorites persistence and isolation | `tests/api/test_workspace_reviews_favorites.py::test_favorites_persist_and_are_isolated` | Automated |
| `TM-API-REVIEW-001` | P1 | Valid review boundaries | `tests/api/test_workspace_reviews_favorites.py::test_review_accepts_rating_and_text_length_boundaries` | Automated |
| `TM-API-REVIEW-002` | P1 | Invalid rating | `tests/api/test_workspace_reviews_favorites.py::test_invalid_review_rating_returns_422` | Automated |
| `TM-API-REVIEW-003` | P1 | Invalid text length | `tests/api/test_workspace_reviews_favorites.py::test_review_text_length_outside_bounds_returns_422` | Automated |
| `TM-API-REVIEW-004` | P1 | Duplicate review | `tests/api/test_workspace_reviews_favorites.py::test_duplicate_review_returns_409` | Automated |
| `TM-API-REVIEW-005` | P1 | Review isolation | `tests/api/test_workspace_reviews_favorites.py::test_review_is_not_visible_in_another_workspace` | Automated |
| `TM-UI-CHECKOUT-001` | P0 | Approved checkout/persistence/cart clear | `tests/ui/test_checkout.py::test_checkout_applies_coupon_persists_order_and_clears_cart` | Automated |
| `TM-UI-CHECKOUT-002` | P1 | Double-submit protection | `tests/ui/test_checkout.py::test_double_submit_guard_creates_only_one_order` | Automated |
| `TM-UI-CHECKOUT-003` | P0 | Declined payment retains cart | `tests/ui/test_checkout.py::test_declined_payment_keeps_cart_and_does_not_create_order` | Automated; execution verification required |
| `TM-UI-FAVORITES-001` | P1 | Favorite toggle and reload persistence | `tests/ui/test_favorites.py::test_favorite_toggle_persists_after_reload` | Automated |

## Framework self-tests

Framework self-tests validate token redaction, UAH parsing, integer rounding, host safety, rate-limit diagnostics, artifact-path sanitization and exception-safe artifact capture.

```bash
python -m pytest tests/unit -q
```

## Maintenance rule

Any pull request that adds, renames, or removes a business test must update this matrix and `docs/test-cases.md`. Confirmed defects must use the `known_defect` marker and `xfail(strict=True)` with the matching `TM-DEF-*` ID.
