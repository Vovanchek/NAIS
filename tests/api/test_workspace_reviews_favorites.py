import pytest

from test_me.api.assertions import assert_status
from test_me.api.client import ApiClient


@pytest.mark.api
@pytest.mark.regression
def test_favorites_persist_and_are_isolated(
    api: ApiClient, api_client: ApiClient
) -> None:
    saved = api.save_favorites(["p01", "p02"])
    assert_status(saved, 200, "Save favorites")
    current = api.favorites()
    assert_status(current, 200, "Read favorites")
    assert current.json()["product_ids"] == ["p01", "p02"]

    workspace_b = api_client.create_workspace()
    assert_status(workspace_b, 201, "Create second workspace")
    other = api_client.request(
        "GET", "/api/favorites", workspace_token=workspace_b.json()["token"]
    )
    assert_status(other, 200, "Read favorites from second workspace")
    assert other.json()["product_ids"] == []


@pytest.mark.api
@pytest.mark.regression
def test_review_accepts_rating_and_text_length_boundaries(api: ApiClient) -> None:
    for product_id, rating, text in (
        ("p01", 1, "x" * 10),
        ("p02", 5, "x" * 500),
    ):
        response = api.save_review(product_id, rating, text)

        assert_status(response, 201, f"Save review boundary for {product_id}")
        saved = api.review(product_id)
        assert_status(saved, 200, "Read saved review")
        assert saved.json()["review"]["rating"] == rating
        assert saved.json()["review"]["text"] == text


@pytest.mark.api
@pytest.mark.negative
def test_invalid_review_rating_returns_422(api: ApiClient) -> None:
    for rating in (0, 6, 2.5):
        response = api.save_review("p01", rating, "Synthetic review text")

        assert_status(response, 422, f"Invalid review rating {rating}")


@pytest.mark.api
@pytest.mark.negative
def test_review_text_length_outside_bounds_returns_422(api: ApiClient) -> None:
    for text in ("x" * 9, "x" * 501, "  xxxxxxxx  "):
        response = api.save_review("p01", 5, text)

        assert_status(response, 422, "Invalid review text length")


@pytest.mark.api
@pytest.mark.regression
def test_duplicate_review_returns_409(api: ApiClient) -> None:
    first = api.save_review("p01", 5, "Synthetic review text")
    assert_status(first, 201, "Create first review")

    duplicate = api.save_review("p01", 4, "Another synthetic review")
    assert_status(duplicate, 409, "Create duplicate review")


@pytest.mark.api
@pytest.mark.regression
def test_review_is_not_visible_in_another_workspace(
    api: ApiClient, api_client: ApiClient
) -> None:
    saved = api.save_review("p01", 5, "Synthetic review text")
    assert_status(saved, 201, "Create review in workspace A")

    workspace_b = api_client.create_workspace()
    assert_status(workspace_b, 201, "Create workspace B")
    other = api_client.request(
        "GET",
        "/api/products/p01/review",
        workspace_token=workspace_b.json()["token"],
    )

    assert_status(other, 200, "Read review from workspace B")
    assert other.json()["review"] is None
