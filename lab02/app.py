"""
Лабораторна робота №2: Модуль із побічними ефектами (І/О, форматування).
"""

from collections.abc import Callable
import time
from core import StockItem, StockSummary, analyze_warehouse, curried_price_multiplier


def get_current_timestamp(time_provider: Callable[[], float] = time.time) -> str:
    """Форматує поточний час для звіту (з підтримкою інжекції часу для тестів)."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_provider()))


def format_summary_report(summary: StockSummary, timestamp: str) -> str:
    """Форматує аналітичний звіт у консольний текстовий вигляд."""
    lines = [
        "=" * 65,
        f"ЗВІТ АНАЛІТИКИ СКЛАДСЬКИХ ЗАПАСІВ ({timestamp})",
        "=" * 65,
        f"Загальна кількість позицій: {summary['total_items_count']}",
        f"Загальна вартість товарів на складі: {summary['total_inventory_value']:.2f} грн",
        "-" * 65,
        "Розподіл позицій за категоріями:",
    ]
    for cat, count in sorted(summary["categories_summary"].items()):
        lines.append(f"  * {cat}: {count} шт.")

    lines.extend([
        "-" * 65,
        "ПОЗИЦІЇ, ЩО ПОТРЕБУЮТЬ ДОЗАМОВЛЕННЯ:",
        f"{'ID':<4} | {'Назва':<20} | {'Залишок':<8} | {'Мін.':<6} | {'Дозамовлення':<12}",
        "-" * 65,
    ])

    if not summary["items_needing_restock"]:
        lines.append("  [Усі позиції в достатній кількості]")
    else:
        for item in summary["items_needing_restock"]:
            lines.append(
                f"{item['id']:<4} | {item['name']:<20} | {item['stock']:<8} | "
                f"{item['min_stock']:<6} | {item['restock_qty']:<12}"
            )

    lines.append("=" * 65)
    return "\n".join(lines)


def run_pipeline() -> None:
    """Запускає повний цикл читання даних, аналізу та виводу."""
    sample_stock: list[StockItem] = [
        {
            "id": 101,
            "name": "ESP32 NodeMCU",
            "stock": 4,
            "price": 180.0,
            "min_stock": 15,
            "category": "Мікроконтролери",
        },
        {
            "id": 102,
            "name": "Сервопривід SG90",
            "stock": 8,
            "price": 65.0,
            "min_stock": 30,
            "category": "Мотори",
        },
        {
            "id": 103,
            "name": "Дисплей OLED 0.96",
            "stock": 25,
            "price": 140.0,
            "min_stock": 10,
            "category": "Дисплеї",
        },
        {
            "id": 104,
            "name": "Патч-корд RJ45 2м",
            "stock": 5,
            "price": 50.0,
            "min_stock": 30,
            "category": "Кабелі",
        },
        {
            "id": 105,
            "name": "Датчик DHT11",
            "stock": 12,
            "price": 85.0,
            "min_stock": 10,
            "category": "Сенсори",
        },
    ]

    # Використання HOF / каррування для 10% інфляційної індексації цін
    inflation_adjuster = curried_price_multiplier(1.10)

    summary = analyze_warehouse(
        sample_stock,
        price_adjuster=inflation_adjuster,
    )

    report_text = format_summary_report(summary, get_current_timestamp())
    print(report_text)