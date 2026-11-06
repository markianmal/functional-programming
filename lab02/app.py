"""
Лабораторна робота №2: Модуль із побічними ефектами (І/О, форматування).
"""

from collections.abc import Callable
import time
from core import StockItem, RestockReport, process_warehouse_pure


def get_current_timestamp(time_provider: Callable[[], float] = time.time) -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_provider()))


def format_report(report: RestockReport, timestamp: str) -> str:
    lines = [
        "=" * 60,
        f"ЗВІТ З ДОЗАМОВЛЕННЯ СКЛАДСЬКИХ ПОЗИЦІЙ ({timestamp})",
        "=" * 60,
        f"{'ID':<4} | {'Назва':<18} | {'К-сть':<6} | {'Разом (з ПДВ)':<12}",
        "-" * 60,
    ]
    for o in report["orders"]:
        lines.append(
            f"{o['id']:<4} | {o['name']:<18} | {o['order_qty']:<6} | {o['final_cost']:<12.2f}"
        )

    lines.extend([
        "-" * 60,
        f"Всього позицій на дозамовлення: {report['items_to_order_count']}",
        f"Загальна кількість одиниць: {report['total_units_to_order']}",
        f"Необхідний бюджет: {report['total_budget_needed']:.2f} грн",
        "=" * 60,
    ])
    return "\n".join(lines)


def run_pipeline() -> None:
    warehouse_stock: list[StockItem] = [
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
    ]

    report = process_warehouse_pure(warehouse_stock)
    print(format_report(report, get_current_timestamp()))