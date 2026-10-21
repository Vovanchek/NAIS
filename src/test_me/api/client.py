from collections.abc import Mapping
from typing import Any

import requests

from test_me.config import Settings


class ApiClient:
    def __init__(self, settings: Settings, workspace_token: str | None = None) -> None:
        self._base_url = settings.base_url
        self._timeout = (settings.api_connect_timeout, settings.api_read_timeout)
        self._session = requests.Session()
        self._workspace_token = workspace_token

    def close(self) -> None:
        self._session.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Mapping[str, Any] | None = None,
        workspace_token: str | None = None,
    ) -> requests.Response:
        token = (
            workspace_token if workspace_token is not None else self._workspace_token
        )
        headers = {"X-Workspace-Token": token} if token else {}
        return self._session.request(
            method,
            f"{self._base_url}{path}",
            params=params,
            json=json,
            headers=headers,
            timeout=self._timeout,
        )

    def health(self) -> requests.Response:
        return self.request("GET", "/api/health")

    def create_workspace(self) -> requests.Response:
        return self.request("POST", "/api/workspaces", workspace_token="")

    def list_products(self, **params: Any) -> requests.Response:
        return self.request("GET", "/api/products", params=params)

    def product(self, product_id: str) -> requests.Response:
        return self.request("GET", f"/api/products/{product_id}")

    def quote(self, payload: Mapping[str, Any]) -> requests.Response:
        return self.request("POST", "/api/quote", json=payload)

    def create_order(self, payload: Mapping[str, Any]) -> requests.Response:
        return self.request("POST", "/api/orders", json=payload)

    def list_orders(self, **params: Any) -> requests.Response:
        return self.request("GET", "/api/orders", params=params)

    def order(self, order_id: str) -> requests.Response:
        return self.request("GET", f"/api/orders/{order_id}")

    def cancel_order(self, order_id: str) -> requests.Response:
        return self.request("POST", f"/api/orders/{order_id}/cancel")

    def favorites(self) -> requests.Response:
        return self.request("GET", "/api/favorites")

    def save_favorites(self, product_ids: list[str]) -> requests.Response:
        return self.request("PUT", "/api/favorites", json={"product_ids": product_ids})

    def review(self, product_id: str) -> requests.Response:
        return self.request("GET", f"/api/products/{product_id}/review")

    def save_review(
        self, product_id: str, rating: int | float, text: str
    ) -> requests.Response:
        return self.request(
            "POST",
            f"/api/products/{product_id}/review",
            json={"rating": rating, "text": text},
        )
