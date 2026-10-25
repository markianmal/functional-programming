"""Точка входу: побудова ієрархічного меню та демонстрація чистих функцій."""

from __future__ import annotations

from evaluator import count_actions, filter_menu_by_role, get_available_actions
from model import Action, Separator, Submenu
from pretty import render_menu


def main() -> None:
    print("=== Лабораторна робота 8: Алгебраїчні типи даних (Варіант 12) ===")

    app_menu = Submenu(
        title="Головне Меню",
        items=(
            Action(title="Довідка", command="help", required_role="guest"),
            Separator(),
            Submenu(
                title="Файл",
                items=(
                    Action(title="Відкрити", command="open_file", required_role="user"),
                    Action(title="Зберегти", command="save_file", required_role="user"),
                    Separator(),
                    Action(
                        title="Налаштування сервера",
                        command="server_config",
                        required_role="admin",
                    ),
                ),
            ),
            Submenu(
                title="Акаунт",
                items=(
                    Action(title="Профіль", command="profile", required_role="user"),
                    Action(
                        title="Видалити користувача",
                        command="delete_user",
                        required_role="admin",
                    ),
                ),
            ),
            Separator(),
            Action(title="Вихід", command="exit", required_role="guest"),
        ),
    )

    print("\n--- Повне дерево меню ---")
    print(render_menu(app_menu))

    print(f"\nЗагальна кількість дій у меню: {count_actions(app_menu)}")

    for role in ("guest", "user", "admin"):
        actions = get_available_actions(app_menu, role)  # type: ignore[arg-type]
        cmd_list = [f"{a.title} ({a.command})" for a in actions]
        print(f"\nДоступні команди для ролі '{role}' ({len(cmd_list)} шт.):")
        for cmd in cmd_list:
            print(f"  * {cmd}")

    print("\n--- Меню після фільтрації для ролі 'guest' ---")
    guest_menu = filter_menu_by_role(app_menu, "guest")
    if guest_menu is not None:
        print(render_menu(guest_menu))


if __name__ == "__main__":
    main()