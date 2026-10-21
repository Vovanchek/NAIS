from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Product:
    id: str
    name: str
    category: str
    price: int
    stock: int

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "Product":
        return cls(
            id=str(payload["id"]),
            name=str(payload["name"]),
            category=str(payload["category"]),
            price=int(payload["price"]),
            stock=int(payload["stock"]),
        )


@dataclass(frozen=True)
class Quote:
    subtotal: int
    discount: int
    shipping: int
    total: int
    currency: str

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "Quote":
        return cls(
            subtotal=int(payload["subtotal"]),
            discount=int(payload["discount"]),
            shipping=int(payload["shipping"]),
            total=int(payload["total"]),
            currency=str(payload["currency"]),
        )
