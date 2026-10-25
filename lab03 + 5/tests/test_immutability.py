"""Tests verifying immutability, hashability, and pure updates."""
from dataclasses import FrozenInstanceError
from types import MappingProxyType
import pytest

from core import (
    add_allergen,
    add_ingredient,
    apply_discount,
    calculate_margin_cached,
    freeze,
    index_by_dish,
    update_meta,
    update_price,
)
from model import Dish, Ingredient, make_meta


@pytest.fixture
def sample_dish() -> Dish:
    i1 = Ingredient(name="Pasta", cost=25.0, weight_grams=150.0)
    i2 = Ingredient(name="Parmesan", cost=40.0, weight_grams=40.0)
    return Dish(
        id=12,
        name="Carbonara",
        price=210.0,
        ingredients=(i1, i2),
        allergens=frozenset({"gluten", "lactose"}),
        meta=make_meta(category="Main", cuisine="Italian"),
    )


def test_no_mutation_when_adding_ingredient(sample_dish: Dish) -> None:
    original = sample_dish
    new_ing = Ingredient(name="Guanciale", cost=55.0, weight_grams=60.0)
    updated = add_ingredient(sample_dish, new_ing)

    assert sample_dish is original
    assert updated is not sample_dish
    assert len(sample_dish.ingredients) == 2
    assert len(updated.ingredients) == 3
    assert updated.total_cost() == sample_dish.total_cost() + 55.0


def test_no_mutation_when_adding_allergen(sample_dish: Dish) -> None:
    updated = add_allergen(sample_dish, "Eggs")
    assert updated is not sample_dish
    assert "eggs" in updated.allergens
    assert "eggs" not in sample_dish.allergens


def test_no_mutation_when_updating_price(sample_dish: Dish) -> None:
    updated = update_price(sample_dish, 260.0)
    assert updated is not sample_dish
    assert sample_dish.price == 210.0
    assert updated.price == 260.0


def test_pure_discount_calculation(sample_dish: Dish) -> None:
    discounted = apply_discount(sample_dish, 10.0)
    assert discounted is not sample_dish
    assert sample_dish.price == 210.0
    assert discounted.price == 189.0


def test_frozen_fields_raise_error(sample_dish: Dish) -> None:
    with pytest.raises(FrozenInstanceError):
        sample_dish.price = 300.0  # type: ignore

    with pytest.raises(FrozenInstanceError):
        sample_dish.name = "Mutated"  # type: ignore


def test_meta_is_strictly_read_only(sample_dish: Dish) -> None:
    with pytest.raises(TypeError):
        sample_dish.meta["category"] = "Snack"  # type: ignore


def test_dish_hashability_and_dict_keys(sample_dish: Dish) -> None:
    # Перевірка хешованості самої страви завдяки field(hash=False) для meta
    other_dish = add_allergen(sample_dish, "peanuts")
    dish_set = {sample_dish, other_dish, sample_dish}
    assert len(dish_set) == 2

    indexed = index_by_dish((sample_dish, other_dish))
    assert sample_dish in indexed
    assert other_dish in indexed
    assert len(indexed) == 2


def test_deep_freeze_utility() -> None:
    raw = {"a": [1, 2], "b": {"c": {3, 4}}}
    frozen = freeze(raw)
    assert isinstance(frozen, MappingProxyType)
    assert isinstance(frozen["a"], tuple)
    assert isinstance(frozen["b"], MappingProxyType)
    assert isinstance(frozen["b"]["c"], frozenset)

    with pytest.raises(TypeError):
        frozen["a"] = (10,)  # type: ignore


def test_lru_cache_optimization() -> None:
    calculate_margin_cached.cache_clear()
    res1 = calculate_margin_cached(250.0, 100.0)
    assert calculate_margin_cached.cache_info().hits == 0
    res2 = calculate_margin_cached(250.0, 100.0)
    assert calculate_margin_cached.cache_info().hits == 1
    assert res1 == res2 == 60.0