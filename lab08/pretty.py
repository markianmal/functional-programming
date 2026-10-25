"""Текстове представлення дерева меню (pretty-print)."""

from __future__ import annotations

from model import Action, MenuItem, Separator, Submenu


def render_menu(item: MenuItem, depth: int = 0) -> str:
    """Рендерить дерево меню у структурований рядок з відступами."""
    indent = "  " * depth
    match item:
        case Action(title=t, command=c, required_role=r):
            return f"{indent}-> [{t}] ({c}) [{r}]"
        case Separator():
            return f"{indent}------------------------"
        case Submenu(title=t, items=children):
            header = f"{indent}[{t}]:"
            if not children:
                return f"{header}\n{indent}  (порожньо)"
            lines = [header]
            for child in children:
                lines.append(render_menu(child, depth + 1))
            return "\n".join(lines)