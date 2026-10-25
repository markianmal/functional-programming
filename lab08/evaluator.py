"""Чисті функції аналізу, фільтрації та обходу дерева меню через match/case."""

from __future__ import annotations

from model import Action, MenuItem, Role, Separator, Submenu

ROLE_HIERARCHY: dict[Role, int] = {
    "guest": 0,
    "user": 1,
    "admin": 2,
}


def is_allowed(user_role: Role, required_role: Role) -> bool:
    """Перевіряє, чи має користувач достатній рівень доступу."""
    return ROLE_HIERARCHY[user_role] >= ROLE_HIERARCHY[required_role]


def get_available_actions(item: MenuItem, role: Role) -> list[Action]:
    """Рекурсивно знаходить усі доступні дії для заданої ролі користувача."""
    match item:
        case Action(title=_, command=_, required_role=req) if is_allowed(role, req):
            return [item]
        case Action():
            return []
        case Separator():
            return []
        case Submenu(title=_, items=children):
            result: list[Action] = []
            for child in children:
                result.extend(get_available_actions(child, role))
            return result


def count_actions(item: MenuItem) -> int:
    """Підраховує сумарну кількість вузлів Action у дереві меню."""
    match item:
        case Action():
            return 1
        case Separator():
            return 0
        case Submenu(items=children):
            return sum(count_actions(child) for child in children)


def filter_menu_by_role(item: MenuItem, role: Role) -> MenuItem | None:
    """Створює нове незмінне дерево меню, що містить лише дозволені пункти."""
    match item:
        case Action(required_role=req) if is_allowed(role, req):
            return item
        case Action():
            return None
        case Separator():
            return item
        case Submenu(title=t, items=children):
            filtered = [
                res
                for child in children
                if (res := filter_menu_by_role(child, role)) is not None
            ]
            return Submenu(title=t, items=tuple(filtered))