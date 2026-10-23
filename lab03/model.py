"""Domain models for restaurant menu (Variant 12)."""
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping, Tuple


def make_meta(**kwargs: str) -> MappingProxyType[str, str]:
    """Create a read-only MappingProxy over an isolated dictionary copy."""
    return MappingProxyType(dict(kwargs))


@dataclass(frozen=True, slots=True)
class Ingredient:
    """Immutable ingredient representation."""

    name: str
    cost: float
    weight_grams: float

    def __post_init__(self) -> None:
        if self.cost < 0:
            raise ValueError("Cost cannot be negative")
        if self.weight_grams <= 0:
            raise ValueError("Weight must be positive")


@dataclass(frozen=True, slots=True)
class Dish:
    """Immutable dish representation."""

    id: int
    name: str
    price: float
    ingredients: Tuple[Ingredient, ...] = ()
    allergens: frozenset[str] = frozenset()
    # mappingproxy не хешується -> виключаємо з hash, але лишаємо в eq
    meta: Mapping[str, str] = field(
        default_factory=lambda: make_meta(), hash=False
    )

    def __post_init__(self) -> None:
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if not isinstance(self.ingredients, tuple):
            raise TypeError("Ingredients must be a tuple")
        if not isinstance(self.allergens, frozenset):
            raise TypeError("Allergens must be a frozenset")
        if not isinstance(self.meta, (MappingProxyType, dict)):
            raise TypeError("Meta must be a Mapping")

    def total_cost(self) -> float:
        """Calculate total prime cost based on ingredients."""
        return sum(item.cost for item in self.ingredients)

    def total_weight(self) -> float:
        """Calculate total dish weight in grams."""
        return sum(item.weight_grams for item in self.ingredients)

    def has_allergen(self, allergen: str) -> bool:
        """Check if allergen is present."""
        return allergen.strip().lower() in {a.lower() for a in self.allergens}