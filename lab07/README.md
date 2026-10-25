# Лабораторна робота №7: functools та operator
**Варіант 12: Навчальні онлайн-курси**

## Архітектура рішення
- `core.py`: конвеєр `pipeline` на основі `functools.reduce`, функції конвеєра `mapf`, `filt` через `functools.partial`, гетери `itemgetter` та маніпуляції з рядками `methodcaller`.
- `loaders.py`: поліморфний завантажувач джерел через `@functools.singledispatch` із підтримкою JSON і CSV для рядків, `pathlib.Path`, відкритих потоків `io.TextIOBase` та списків словників.
- `models.py`: модель `CourseRank` із `@functools.total_ordering`, що забезпечує коректне лінійне впорядкування курсів (`rating` ↓, `students` ↓, `title` ↑).
- `main.py`: демонстрація завантаження, ранжування та селекторів.
- `tests/`: 24 модульні та property-тести.

## Запуск та перевірка
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Демонстраційний запуск
python main.py

# Тестування
pytest -v

# Статичний аналіз
mypy .
ruff check .
black --check .