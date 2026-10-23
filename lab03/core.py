"""Pure business functions, immutable updates and utilities (Variant 12)."""
from collections.abc import Mapping
from dataclasses import replace
from functools import lru_cache
from types import MappingProxyType
from typing import Any, Mapping as TMapping, Union

from model import Dish, Ingredient


def add_ingredient(
    dish: Dish,
    ingredient_or_name: Union[Ingredient, str],
    cost: float = 0.0,
    weight_grams: float = 0.0,
) -> Dish:
    """Pure update: add ingredient passing either an Ingredient instance or fields."""
    if isinstance(ingredient_or_name, Ingredient):
        new_item = ingredient_or_name
    else:
        new_item = Ingredient(ingredient_or_name, cost, weight_grams)
    return replace(dish, ingredients=dish.ingredients + (new_item,))


def add_allergen(dish: Dish, allergen: str) -> Dish:
    """Pure update: return a new Dish with allergen added to frozenset."""
    new_allergens = dish.allergens | frozenset({allergen.strip().lower()})
    return replace(dish, allergens=new_allergens)


def update_price(dish: Dish, new_price: float) -> Dish:
    """Pure update: return a new Dish with updated price."""
    if new_price < 0:
        raise ValueError("Price cannot be negative")
    return replace(dish, price=new_price)


def update_meta(dish: Dish, **new_meta_entries: str) -> Dish:
    """Pure update: return a new Dish with merged read-only metadata."""
    merged = dict(dish.meta)
    merged.update(new_meta_entries)
    return replace(dish, meta=MappingProxyType(merged))


def with_meta(dish: Dish, **new_meta_entries: str) -> Dish:
    """Alias for update_meta."""
    return update_meta(dish, **new_meta_entries)


def apply_discount(dish: Dish, discount_percent: float) -> Dish:
    """Pure update: return a new Dish with discounted price."""
    if not (0.0 <= discount_percent <= 100.0):
        raise ValueError("Discount percent must be between 0 and 100")
    discounted = round(dish.price * (1.0 - discount_percent / 100.0), 2)
    return replace(dish, price=discounted)


def index_by_dish(dishes: tuple[Dish, ...]) -> TMapping[Dish, float]:
    """Demonstrate dish hashability as dictionary key."""
    return MappingProxyType(
        {d: calculate_margin_cached(d.price, d.total_cost()) for d in dishes}
    )


def freeze(obj: Any) -> Any:
    """Deeply freeze nested mutable structures into immutable equivalents."""
    if isinstance(obj, MappingProxyType):
        return obj
    if isinstance(obj, Mapping):
        return MappingProxyType({k: freeze(v) for k, v in obj.items()})
    if isinstance(obj, (set, frozenset)):
        return frozenset(freeze(x) for x in obj)
    if isinstance(obj, (list, tuple)):
        return tuple(freeze(x) for x in obj)
    return obj


@lru_cache(maxsize=1024)
def calculate_margin_cached(price: float, cost: float) -> float:
    """Cached pure calculation for profit margin."""
    if price <= 0:
        return 0.0
    return round(((price - cost) / price) * 100.0, 2)