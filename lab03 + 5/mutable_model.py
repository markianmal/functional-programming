"""Mutable model representation for performance benchmarking (Variant 12)."""
from typing import Any, Dict


def make_dish_dict(id: int, name: str, price: float) -> Dict[str, Any]:
    return {
        "id": id,
        "name": name,
        "price": price,
        "ingredients": [],
        "allergens": set(),
        "meta": {},
    }


def add_ingredient_inplace(
    dish: Dict[str, Any], name: str, cost: float, weight: float
) -> None:
    dish["ingredients"].append({"name": name, "cost": cost, "weight": weight})


def add_allergen_inplace(dish: Dict[str, Any], allergen: str) -> None:
    dish["allergens"].add(allergen.lower())


def calculate_margin_dict(price: float, cost: float) -> float:
    if price <= 0:
        return 0.0
    return round(((price - cost) / price) * 100, 2)