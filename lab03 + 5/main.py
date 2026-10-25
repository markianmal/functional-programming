"""Main demonstration script."""
from core import (
    add_allergen,
    add_ingredient,
    calculate_margin_cached,
    index_by_dish,
    with_meta,
)
from model import Dish, Ingredient, make_meta


def main() -> None:
    d0 = Dish(
        id=1,
        name="Pasta Carbonara",
        price=220.0,
        ingredients=(Ingredient("Pasta", 30.0, 150.0),),
        allergens=frozenset({"gluten"}),
        meta=make_meta(cuisine="Italian"),
    )
    d1 = add_ingredient(d0, Ingredient("Guanciale", 60.0, 70.0))
    d2 = add_allergen(d1, "lactose")
    d3 = with_meta(d2, chef="Mario")

    print(f"d0 is d3: {d0 is d3} | d0 unchanged: {len(d0.ingredients) == 1}")
    print(f"Margin: {calculate_margin_cached(d3.price, d3.total_cost())}%")
    print("Cache info:", calculate_margin_cached.cache_info())
    idx = index_by_dish((d0, d3))
    print(f"Indexed {len(idx)} dishes successfully as dict keys.")


if __name__ == "__main__":
    main()