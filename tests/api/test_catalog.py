import pytest

from test_me.api.assertions import assert_status
from test_me.api.client import ApiClient
from test_me.api.models import Product


def all_products(api: ApiClient) -> list[Product]:
    response = api.list_products(limit=20)
    assert_status(response, 200, "List catalog")
    return [Product.from_payload(item) for item in response.json()["items"]]


@pytest.mark.api
def test_category_filter_returns_only_requested_category(api: ApiClient) -> None:
    for category in ("Audio", "Workspace", "Lifestyle"):
        response = api.list_products(category=category, limit=20)

        assert_status(response, 200, f"Category filter {category}")
        assert response.json()["items"]
        assert {item["category"] for item in response.json()["items"]} == {category}


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.known_defect
@pytest.mark.xfail(strict=True, reason="TM-DEF-004: catalog search is case-sensitive")
def test_search_is_case_insensitive_and_trims_query(api: ApiClient) -> None:
    product = next(item for item in all_products(api) if item.stock > 0)
    query = product.name[:4]
    results = []

    for value in (query, query.swapcase(), f"  {query}  "):
        response = api.list_products(q=value, limit=20)
        results.append((value, response))

    failures = []
    for value, response in results:
        if response.status_code != 200:
            failures.append(f"{value!r}: HTTP {response.status_code}")
            continue
        ids = {item["id"] for item in response.json()["items"]}
        if product.id not in ids:
            failures.append(f"{value!r}: product {product.id} missing")
    assert not failures, "Catalog search normalization failed: " + "; ".join(failures)


@pytest.mark.api
@pytest.mark.regression
def test_in_stock_filter_excludes_zero_stock_products(api: ApiClient) -> None:
    response = api.list_products(in_stock=True, limit=20)

    assert_status(response, 200, "In-stock filter")
    assert all(item["stock"] > 0 for item in response.json()["items"])


@pytest.mark.api
@pytest.mark.regression
def test_price_bounds_are_inclusive(api: ApiClient) -> None:
    product = next(item for item in all_products(api) if item.stock > 0)
    response = api.list_products(
        min_price=product.price,
        max_price=product.price,
        limit=20,
    )

    assert_status(response, 200, "Inclusive price bounds")
    assert product.id in {item["id"] for item in response.json()["items"]}
    assert all(item["price"] == product.price for item in response.json()["items"])


@pytest.mark.api
@pytest.mark.negative
def test_min_price_greater_than_max_price_returns_422(api: ApiClient) -> None:
    response = api.list_products(min_price=200_000, max_price=100_000)

    assert_status(response, 422, "Invalid price range")


@pytest.mark.api
@pytest.mark.regression
def test_price_sort_is_numeric(api: ApiClient) -> None:
    for sort, reverse in (("price_asc", False), ("price_desc", True)):
        response = api.list_products(sort=sort, page=1, limit=20)

        assert_status(response, 200, f"Sort products by {sort}")
        prices = [item["price"] for item in response.json()["items"]]
        assert prices == sorted(prices, reverse=reverse)


@pytest.mark.api
@pytest.mark.regression
def test_pagination_and_limit_boundaries(api: ApiClient) -> None:
    first = api.list_products(page=1, limit=1)
    second = api.list_products(page=2, limit=1)
    max_limit = api.list_products(page=1, limit=20)

    for response, expected_limit in ((first, 1), (second, 1), (max_limit, 20)):
        assert_status(response, 200, "Catalog pagination")
        assert response.json()["limit"] == expected_limit
    assert first.json()["items"][0]["id"] != second.json()["items"][0]["id"]

    for invalid_limit in (0, 21):
        invalid = api.list_products(limit=invalid_limit)
        assert_status(invalid, 422, f"Invalid page limit {invalid_limit}")


@pytest.mark.api
@pytest.mark.regression
def test_combined_catalog_filters(api: ApiClient) -> None:
    product = next(item for item in all_products(api) if item.stock > 0)
    response = api.list_products(
        q=product.name[:4],
        category=product.category,
        sort="price_asc",
        page=1,
        limit=20,
        in_stock=True,
        min_price=product.price,
        max_price=product.price,
    )

    assert_status(response, 200, "Combined catalog filters")
    matches = response.json()["items"]
    assert product.id in {item["id"] for item in matches}
    assert all(
        item["category"] == product.category
        and item["stock"] > 0
        and item["price"] == product.price
        for item in matches
    )
