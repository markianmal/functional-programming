"""Демонстраційний скрипт: замикання, декоратори та композиція."""

from __future__ import annotations

from closures import make_converter, make_counter, make_logger
from decorators import cached, count_calls, timed


def main() -> None:
    print("=== Лабораторна робота 6: Замикання та Декоратори ===")
    counter = make_counter(start=10)
    print("make_counter:", counter(), counter(), counter())

    usd_to_uah = make_converter(scale=41.5, precision=2)
    print("make_converter (100 USD):", usd_to_uah(100.0), "UAH")

    logs: list[str] = []
    logger = make_logger("DATA_CONV", sink=logs.append)

    @timed("rate-calc", unit="ms", logger=logger)
    @count_calls()
    @cached(ttl=5.0)
    def get_currency_rate(pair: str) -> float:
        return 41.50 if pair == "USD_UAH" else 45.20

    print("Виклик 1:", get_currency_rate("USD_UAH"))
    print("Виклик 2 (кеш):", get_currency_rate("USD_UAH"))
    print("Статистика кешу:", get_currency_rate.cache_info())
    print("Кількість викликів через count_calls:", get_currency_rate.calls())

    removed = get_currency_rate.cache_invalidate(lambda args, kw: args == ("USD_UAH",))
    print(f"Інвалідовано ключів: {removed}")
    print("Виклик 3 після інвалідації:", get_currency_rate("USD_UAH"))
    print("Оновлена статистика кешу:", get_currency_rate.cache_info())


if __name__ == "__main__":
    main()