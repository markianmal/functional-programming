# Лабораторна робота №8: Алгебраїчні типи даних (ADT) "по-Python'івськи"
**Варіант 12: Дерево меню застосунку**

## Опис реалізації
- `model.py`: незмінні dataclass-вузли `Action`, `Separator` та рекурсивний `Submenu`. Сума типів `MenuItem: TypeAlias = Action | Separator | Submenu`. Фіксація ролей через `Literal["guest", "user", "admin"]` та структурний протокол `Renderable` через `typing.Protocol`.
- `evaluator.py`: чисті функції аналізу структури меню через `match/case` (`get_available_actions`, `count_actions`, `filter_menu_by_role`) без імперативних перевірок `isinstance`.
- `pretty.py`: ієрархічне текстове відображення дерева меню з відступами.
- `main.py`: демонстрація побудови дерева, рендерингу та фільтрації за рівнями доступу.
- `tests/`: 22 тести (`pytest` + `hypothesis`), перевірка незмінності вузлів та коректності структурного патерн-матчингу.

## Швидкий запуск
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Запуск демонстрації
python main.py

# Модульне тестування
pytest -v

# Строгий статичний аналіз типів та стиль
mypy --strict .
ruff check .
black --check .