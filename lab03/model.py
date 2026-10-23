"""Доменні сутності ресторанного меню (Варіант 12).

Використано @dataclass(frozen=True, slots=True), tuple, frozenset та MappingProxyType.
"""
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping, Tuple


def make_meta(**kwargs: str) -> MappingProxyType[str, str]:
    """Створює read-only MappingProxy поверх ізольованої копії словника."""
    return MappingProxyType(dict(kwargs))


@dataclass(frozen=True, slots=True)
class Ingredient:
    """Незмінна модель інгредієнта страви."""

    name: str
    cost: float
    weight_grams: float

    def __post_init__(self) -> None:
        if self.cost < 0:
            raise ValueError("Cost cannot be negative")
        if self.weight_grams <= 0:
            raise ValueError("Weight must be strictly positive")


@dataclass(frozen=True, slots=True)
class Dish:
    """Незмінна модель ресторанної страви."""

    id: int
    name: str
    price: float
    ingredients: Tuple[Ingredient, ...]
    allergens: frozenset[str]
    meta: Mapping[str, str]

    def __post_init__(self) -> None:
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if not isinstance(self.ingredients, tuple):
            raise TypeError("Field 'ingredients' must be a tuple")
        if not isinstance(self.allergens, frozenset):
            raise TypeError("Field 'allergens' must be a frozenset")
        if not isinstance(self.meta, (MappingProxyType, dict)):
            raise TypeError("Field 'meta' must be a Mapping")

    def total_cost(self) -> float:
        """Розрахунок собівартості на основі списку інгредієнтів."""
        return sum(item.cost for item in self.ingredients)

    def total_weight(self) -> float:
        """Розрахунок загальної ваги страви в грамах."""
        return sum(item.weight_grams for item in self.ingredients)

    def has_allergen(self, allergen: str) -> bool:
        """Перевірка наявності алергену."""
        return allergen.strip().lower() in {a.lower() for a in self.allergens}