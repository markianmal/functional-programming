"""Чисті функції оновлення (pure updates) та бізнес-логіка меню."""
from collections.abc import Mapping
from dataclasses import replace
from functools import lru_cache
from types import MappingProxyType
from typing import Any

from model import Dish, Ingredient


def add_ingredient(dish: Dish, ingredient: Ingredient) -> Dish:
    """Pure update: повертає новий об'єкт Dish із доданим інгредієнтом."""
    new_ingredients = dish.ingredients + (ingredient,)
    return replace(dish, ingredients=new_ingredients)


def add_allergen(dish: Dish, allergen: str) -> Dish:
    """Pure update: повертає новий Dish з доданим алергеном."""
    cleaned = allergen.strip().lower()
    new_allergens = dish.allergens | frozenset({cleaned})
    return replace(dish, allergens=new_allergens)


def update_price(dish: Dish, new_price: float) -> Dish:
    """Pure update: повертає новий Dish зі зміненою ціною."""
    if new_price < 0:
        raise ValueError("Price cannot be negative")
    return replace(dish, price=new_price)


def update_meta(dish: Dish, **new_meta: str) -> Dish:
    """Pure update: повертає новий Dish з оновленими метаданими."""
    merged = dict(dish.meta)
    merged.update(new_meta)
    return replace(dish, meta=MappingProxyType(merged))


def apply_discount(dish: Dish, percent: float) -> Dish:
    """Pure update: розрахунок акційної ціни без зміни оригіналу."""
    if not (0.0 <= percent <= 100.0):
        raise ValueError("Discount must be between 0 and 100 percent")
    new_price = round(dish.price * (1.0 - percent / 100.0), 2)
    return replace(dish, price=new_price)


def freeze(obj: Any) -> Any:
    """Глибоке заморожування вкладених структур даних."""
    if isinstance(obj, MappingProxyType):
        return obj
    if isinstance(obj, Mapping):
        return MappingProxyType({k: freeze(v) for k, v in obj.items()})
    if isinstance(obj, (set, frozenset)):
        return frozenset(freeze(x) for x in obj)
    if isinstance(obj, (list, tuple)):
        return tuple(freeze(x) for x in obj)
    return obj


@lru_cache(maxsize=256)
def calculate_margin_cached(price: float, cost: float) -> float:
    """Кешований розрахунок маржинальності для чистих значень."""
    if price <= 0:
        return 0.0
    return round(((price - cost) / price) * 100.0, 2)