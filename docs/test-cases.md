# Test Cases

Each business-facing automated test has one stable test case ID, one primary GitHub Issue, and one exact pytest node ID. Confirmed defects retain the required behavior as the expected result and are tracked separately in [`defects.md`](defects.md).

| ID | Requirement / behavior and expected result | Priority / type | Exact pytest node ID | GitHub Issue |
|---|---|---|---|---:|
| TM-API-AUTH-001 | Missing and invalid workspace tokens are rejected on stateful endpoints; each request returns HTTP 401. | P0 / negative API | `tests/api/test_authorization.py::test_stateful_endpoints_reject_missing_and_invalid_tokens` | #5 |
| TM-API-CATALOG-001 | Category filters return only products from the requested category. | P1 / API regression | `tests/api/test_catalog.py::test_category_filter_returns_only_requested_category` | #16 |
| TM-API-CATALOG-002 | Search is case-insensitive and trims surrounding whitespace; normalized queries return the selected product. Known defect TM-DEF-004. | P1 / API regression | `tests/api/test_catalog.py::test_search_is_case_insensitive_and_trims_query` | #27 |
| TM-API-CATALOG-003 | In-stock filtering excludes all zero-stock products. | P1 / API regression | `tests/api/test_catalog.py::test_in_stock_filter_excludes_zero_stock_products` | #28 |
| TM-API-CATALOG-004 | Minimum and maximum price bounds are inclusive. | P1 / API regression | `tests/api/test_catalog.py::test_price_bounds_are_inclusive` | #29 |
| TM-API-CATALOG-005 | A minimum price greater than the maximum returns HTTP 422. | P1 / negative API | `tests/api/test_catalog.py::test_min_price_greater_than_max_price_returns_422` | #30 |
| TM-API-CATALOG-006 | Ascending and descending price sorts order prices numerically. | P1 / API regression | `tests/api/test_catalog.py::test_price_sort_is_numeric` | #31 |
| TM-API-CATALOG-007 | Valid pagination and limit boundaries return the requested limits and distinct page items; invalid limits return HTTP 422. | P1 / API regression | `tests/api/test_catalog.py::test_pagination_and_limit_boundaries` | #32 |
| TM-API-CATALOG-008 | Combined query, category, stock, price, and sort filters return items satisfying every requested filter. | P1 / API regression | `tests/api/test_catalog.py::test_combined_catalog_filters` | #33 |
| TM-API-ORDER-001 | An approved order is created as confirmed; quote, order, list, and detail totals match independent calculations; first cancellation returns HTTP 200 and `cancelled`. | P0 / API regression | `tests/api/test_orders.py::test_approved_order_lifecycle_and_repeat_cancel_conflict` | #19 |
| TM-API-ORDER-002 | Repeating cancellation of an already-cancelled order returns HTTP 409. Known defect TM-DEF-003. | P0 / negative API regression | `tests/api/test_orders.py::test_repeated_order_cancellation_returns_conflict` | #40 |
| TM-API-ORDER-003 | Declined payment returns HTTP 402, creates no order, and leaves product stock unchanged. | P0 / negative API | `tests/api/test_orders.py::test_declined_payment_does_not_create_order` | #18 |
| TM-API-ORDER-004 | An order in one workspace is not visible in another workspace; foreign detail returns HTTP 404. | P1 / negative API | `tests/api/test_orders.py::test_order_is_not_visible_from_another_workspace` | #17 |
| TM-API-QUOTE-001 | Coupon matching ignores case and surrounding whitespace; each valid variant yields independently calculated UAH totals. Known defect TM-DEF-001. | P0 / API regression | `tests/api/test_quote.py::test_welcome_coupon_is_case_and_whitespace_insensitive` | #14 |
| TM-API-QUOTE-002 | An unknown coupon returns HTTP 422. | P0 / negative API | `tests/api/test_quote.py::test_unknown_coupon_is_rejected` | #13 |
| TM-API-QUOTE-003 | Standard shipping is free at and above 150000 kopecks and costs 8000 below the threshold. Known defect TM-DEF-002. | P0 / API regression | `tests/api/test_quote.py::test_standard_shipping_threshold_is_inclusive` | #12 |
| TM-API-QUOTE-004 | Coupon discounts apply to goods, not delivery; standard and express delivery charges remain correct. | P0 / API regression | `tests/api/test_quote.py::test_delivery_charge_is_not_discounted` | #11 |
| TM-API-QUOTE-005 | Quantities 1 and 10 are quoted when stock allows; subtotal and total are calculated correctly. | P0 / API regression | `tests/api/test_quote.py::test_valid_quantity_boundaries_are_quoted` | #10 |
| TM-API-QUOTE-006 | Quantities outside schema bounds (0 and 11) return HTTP 422. | P0 / negative API | `tests/api/test_quote.py::test_quantity_outside_schema_bounds_returns_422` | #34 |
| TM-API-QUOTE-007 | Requesting more than available positive stock returns HTTP 409. | P0 / negative API | `tests/api/test_quote.py::test_stock_shortage_returns_409` | #35 |
| TM-API-QUOTE-008 | Quoting a zero-stock product returns HTTP 409. | P0 / negative API | `tests/api/test_quote.py::test_out_of_stock_product_cannot_be_quoted` | #36 |
| TM-API-SMOKE-001 | The health endpoint returns HTTP 200 with status, version, and seed. | P0 / API smoke | `tests/api/test_smoke.py::test_health_endpoint_reports_service_status` | #8 |
| TM-API-WORKSPACE-001 | Workspace creation returns HTTP 201 and a token, with no request body or authorization/workspace-token request headers. | P0 / API smoke | `tests/api/test_smoke.py::test_create_workspace_returns_token_without_authorization` | #9 |
| TM-API-CATALOG-009 | Catalog listing returns valid metadata and product detail matching the listed item. | P0 / API smoke | `tests/api/test_smoke.py::test_catalog_lists_products_and_product_detail` | #7 |
| TM-API-AUTH-002 | Protected order listing rejects both missing and invalid workspace tokens with HTTP 401. | P0 / negative API | `tests/api/test_smoke.py::test_protected_orders_reject_missing_and_invalid_workspace_tokens` | #6 |
| TM-API-FAVORITES-001 | Favorites persist in one workspace and remain empty in a separate workspace. | P1 / API regression | `tests/api/test_workspace_reviews_favorites.py::test_favorites_persist_and_are_isolated` | #26 |
| TM-API-REVIEW-001 | Reviews accept rating/text boundaries and persist the submitted boundary values. | P1 / API regression | `tests/api/test_workspace_reviews_favorites.py::test_review_accepts_rating_and_text_length_boundaries` | #15 |
| TM-API-REVIEW-002 | Ratings 0, 6, and 2.5 are rejected with HTTP 422. | P1 / negative API | `tests/api/test_workspace_reviews_favorites.py::test_invalid_review_rating_returns_422` | #37 |
| TM-API-REVIEW-003 | Review text below/above supported length bounds, including whitespace-padded too-short text, returns HTTP 422. | P1 / negative API | `tests/api/test_workspace_reviews_favorites.py::test_review_text_length_outside_bounds_returns_422` | #38 |
| TM-API-REVIEW-004 | A second review for the same product/workspace returns HTTP 409. | P1 / API regression | `tests/api/test_workspace_reviews_favorites.py::test_duplicate_review_returns_409` | #20 |
| TM-API-REVIEW-005 | A review saved in one workspace is returned as `review=null` in another workspace. | P1 / API regression | `tests/api/test_workspace_reviews_favorites.py::test_review_is_not_visible_in_another_workspace` | #39 |
| TM-UI-CHECKOUT-001 | Approved checkout creates one confirmed order with independently calculated totals, persists after reload, and clears the cart. | P0 / UI smoke regression | `tests/ui/test_checkout.py::test_checkout_applies_coupon_persists_order_and_clears_cart` | #21 |
| TM-UI-CHECKOUT-002 | Synchronous double submission creates exactly one order. | P1 / UI regression | `tests/ui/test_checkout.py::test_double_submit_guard_creates_only_one_order` | #23 |
| TM-UI-CHECKOUT-003 | Declined payment displays an error, creates no order, and preserves the cart. | P0 / negative UI regression | `tests/ui/test_checkout.py::test_declined_payment_keeps_cart_and_does_not_create_order` | #41 |
| TM-UI-CHECKOUT-004 | Approved checkout with express delivery creates one confirmed order, applies express shipping total, and persists after reload. | P0 / UI regression | `tests/ui/test_checkout_additional_e2e.py::test_checkout_express_delivery_creates_confirmed_order` | #42 |
| TM-UI-CHECKOUT-005 | Checkout with a tampered invalid payment value displays an error, creates no order, and keeps cart contents. | P0 / negative UI regression | `tests/ui/test_checkout_additional_e2e.py::test_checkout_rejects_invalid_payment_value_without_creating_order` | #43 |
| TM-UI-FAVORITES-001 | A dynamically selected catalog product's favorite state toggles, persists after reload, then toggles off. | P1 / UI regression | `tests/ui/test_favorites.py::test_favorite_toggle_persists_after_reload` | #24 |

Framework unit tests do not have business test-case Issues; see the separate **Framework self-tests** section in [`traceability.md`](traceability.md).
