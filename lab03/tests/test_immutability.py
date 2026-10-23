"""Тести перевірки референтної прозорості, відсутності мутацій та типування."""
from copy import deepcopy
from dataclasses import FrozenInstanceError
from types import MappingProxyType
import pytest

from core import (
    add_allergen,
    add_ingredient,
    apply_discount,
    calculate_margin_cached,
    freeze,
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
    original_ingredients_count = len(sample_dish.ingredients)
    original_total_cost = sample_dish.total_cost()
    new_ing = Ingredient(name="Guanciale", cost=55.0, weight_grams=60.0)

    updated = add_ingredient(sample_dish, new_ing)

    # Перевірка референтної прозорості та відсутності мутацій
    assert sample_dish is original
    assert updated is not sample_dish
    assert len(sample_dish.ingredients) == original_ingredients_count
    assert sample_dish.total_cost() == original_total_cost
    assert len(updated.ingredients) == original_ingredients_count + 1
    assert updated.total_cost() == original_total_cost + 55.0


def test_no_mutation_when_adding_allergen(sample_dish: Dish) -> None:
    updated = add_allergen(sample_dish, "Eggs")

    assert updated is not sample_dish
    assert "eggs" in updated.allergens
    assert "eggs" not in sample_dish.allergens
    assert sample_dish.allergens == frozenset({"gluten", "lactose"})


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


def test_frozen_dataclass_raises_on_direct_mutation(sample_dish: Dish) -> None:
    with pytest.raises(FrozenInstanceError):
        sample_dish.price = 300.0  # type: ignore

    with pytest.raises(FrozenInstanceError):
        sample_dish.name = "Mutated"  # type: ignore


def test_mappingproxy_is_strictly_read_only(sample_dish: Dish) -> None:
    with pytest.raises(TypeError):
        sample_dish.meta["category"] = "Snack"  # type: ignore


def test_ingredient_hashability() -> None:
    i1 = Ingredient(name="Olive Oil", cost=15.0, weight_grams=20.0)
    i2 = Ingredient(name="Olive Oil", cost=15.0, weight_grams=20.0)
    ingredient_set = {i1, i2}

    assert len(ingredient_set) == 1
    assert hash(i1) == hash(i2)


def test_deep_freeze_utility() -> None:
    raw_payload = {
        "menu_section": "Breakfast",
        "tags": ["morning", "special"],
        "ingredients": [{"name": "Egg", "cost": 10.0}],
        "allergens": {"eggs", "dairy"},
    }
    frozen = freeze(raw_payload)

    assert isinstance(frozen, MappingProxyType)
    assert isinstance(frozen["tags"], tuple)
    assert isinstance(frozen["allergens"], frozenset)
    assert isinstance(frozen["ingredients"], tuple)
    assert isinstance(frozen["ingredients"][0], MappingProxyType)

    with pytest.raises(TypeError):
        frozen["menu_section"] = "Dinner"  # type: ignore


def test_lru_cache_optimization() -> None:
    calculate_margin_cached.cache_clear()

    res1 = calculate_margin_cached(250.0, 100.0)
    info1 = calculate_margin_cached.cache_info()
    assert info1.hits == 0

    res2 = calculate_margin_cached(250.0, 100.0)
    info2 = calculate_margin_cached.cache_info()
    assert info2.hits == 1
    assert res1 == res2 == 60.0