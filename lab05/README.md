# Лабораторна робота №5: Ліниві обчислення, генератори та itertools
**Варіант 12: Потік трикутних чисел**

## Реалізовані модулі
- `streams.py` — нескінченний стрім Фібоначчі (`fib_stream`), нескінченний лічильник (`naturals`), ковзне вікно без повної матеріалізації (`sliding_window`), рухоме середнє (`moving_average`), утиліти вибірки та пропуску (`take`, `drop`).
- `triangular_numbers.py` — нескінченний лінивий потік трикутних чисел $T_n = \sum_{i=1}^n i$ через `itertools.count` та `itertools.accumulate`, фільтрація до заданої межі через `takewhile`, обчислення різниць сусідніх значень за допомогою `sliding_window(k=2)`.
- `main.py` — демонстраційний сценарій запуску.
- `tests/` — модульні та property-based тести на pytest та Hypothesis, включаючи перевірку лінивості (evaluation count).

## Швидкий запуск
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Запуск демонстрації
python main.py

# Запуск тестів
pytest -v

# Статичний аналіз та перевірка стилю
mypy .
ruff check .
black --check .