"""Алгебраїчні типи даних (ADT) дерева меню застосунку (Варіант 12)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol, TypeAlias

# Literal для фіксації ролей користувачів
Role: TypeAlias = Literal["guest", "user", "admin"]


class Renderable(Protocol):
    """Структурний протокол для об'єктів, що підтримують відтворення у вигляді тексту."""

    def render(self, depth: int = 0) -> str: ...


@dataclass(frozen=True)
class Action:
    """Кінцевий вузол меню: конкретна дія/команда."""

    title: str
    command: str
    required_role: Role = "guest"


@dataclass(frozen=True)
class Separator:
    """Вузол візуального роздільника пунктів меню."""

    pass


@dataclass(frozen=True)
class Submenu:
    """Рекурсивний вузол: контейнер підпунктів меню."""

    title: str
    items: tuple[MenuItem, ...]


# Сума типів (ADT) для елемента меню
MenuItem: TypeAlias = Action | Separator | Submenu

# Явні аргументи для оптимізованого позиційного зіставлення в match/case
Action.__match_args__ = ("title", "command", "required_role")
Separator.__match_args__ = ()
Submenu.__match_args__ = ("title", "items")