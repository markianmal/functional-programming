"""Оболонка побічних ефектів (I/O shell) для взаємодії з користувачем."""

from collections.abc import Callable
import time
from core import (
    RestockReport,
    StockItem,
    make_restock_processor,
)


def get_current_timestamp(time_provider: Callable[[], float] = time.time) -> str:
    """Отримує час через dependency injection (time_provider), усуваючи приховані ефекти."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_provider()))


def format_report(report: RestockReport, timestamp: str) -> str:
    """Чисте форматування рядка звіту (без print всередині)."""
    lines = [
        "=" * 60,
        f"ЗВІТ З ДОЗАМОВЛЕННЯ СКЛАДСЬКИХ ПОЗИЦІЙ ({timestamp})",
        "=" * 60,
        f"{'ID':<4} | {'Назва':<18} | {'К-сть':<6} | {'Ціна':<8} | {'Разом (з ПДВ)':<12}",
        "-" * 60,
    ]

    for o in report["orders"]:
        lines.append(
            f"{o['id']:<4} | {o['name']:<18} | {o['order_qty']:<6} | "
            f"{o['unit_price']:<8.2f} | {o['final_cost']:<12.2f}"
        )

    lines.extend(
        [
            "-" * 60,
            f"Всього позицій на дозамовлення: {report['items_to_order_count']}",
            f"Загальна кількість одиниць:    {report['total_units_to_order']}",
            f"Необхідний бюджет:             {report['total_budget_needed']:.2f} грн",
            "=" * 60,
        ]
    )
    return "\n".join(lines)


def run_pipeline() -> None:
    """I/O-оболонка: ініціалізує дані, запускає обчислення і виводить результат."""
    warehouse_stock: list[StockItem] = [
        {
            "id": 101,
            "name": "ESP32 NodeMCU",
            "stock": 4,
            "price": 180.0,
            "min_stock": 15,
            "category": "Electronics",
        },
        {
            "id": 102,
            "name": "Сервопривід SG90",
            "stock": 3,
            "price": 65.0,
            "min_stock": 25,
            "category": "Motors",
        },
        {
            "id": 103,
            "name": "Step-Down LM2596",
            "stock": 22,
            "price": 45.0,
            "min_stock": 20,
            "category": "Power",
        },
        {
            "id": 104,
            "name": "Патч-корд RJ45 2м",
            "stock": 5,
            "price": 50.0,
            "min_stock": 30,
            "category": "Cables",
        },
        {
            "id": 105,
            "name": "Датчик DS18B20",
            "stock": 12,
            "price": 75.0,
            "min_stock": 10,
            "category": "Sensors",
        },
    ]

    # Складання налаштованого процесора через фабрику
    custom_processor = make_restock_processor(
        should_restock=lambda item: item["stock"] < item["min_stock"],
        calc_qty=lambda item: item["min_stock"] - item["stock"],
        discount_policy=lambda cost, qty: cost * 0.90 if qty >= 20 else cost,
        tax_policy=lambda amount: amount * 1.20,
    )

    report = custom_processor(warehouse_stock)
    rendered_output = format_report(report, timestamp=get_current_timestamp())

    # Єдине місце з побічним ефектом виводу на екран
    print(rendered_output)


if __name__ == "__main__":
    run_pipeline()