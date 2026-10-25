"""Модульні та property-based тести для перевірки ADT дерева меню."""

from __future__ import annotations

import timeit
from dataclasses import FrozenInstanceError
from hypothesis import given
from hypothesis import strategies as st
import pytest
from evaluator import count_actions, filter_menu_by_role, get_available_actions, is_allowed
from model import Action, MenuItem, Role, Separator, Submenu
from pretty import render_menu


def sample_menu() -> Submenu:
    return Submenu(
        title="Root",
        items=(
            Action(title="A1", command="cmd1", required_role="guest"),
            Separator(),
            Submenu(
                title="Sub",
                items=(
                    Action(title="A2", command="cmd2", required_role="user"),
                    Action(title="A3", command="cmd3", required_role="admin"),
                ),
            ),
        ),
    )


def test_action_node_immutability() -> None:
    act = Action(title="Test", command="cmd", required_role="user")
    assert act.title == "Test"
    with pytest.raises(FrozenInstanceError):
        act.title = "New"  # type: ignore[misc]


def test_separator_node() -> None:
    sep = Separator()
    assert isinstance(sep, Separator)


def test_submenu_nested_structure() -> None:
    menu = sample_menu()
    assert menu.title == "Root"
    assert len(menu.items) == 3


def test_get_available_actions_guest() -> None:
    actions = get_available_actions(sample_menu(), "guest")
    assert [a.command for a in actions] == ["cmd1"]


def test_get_available_actions_user() -> None:
    actions = get_available_actions(sample_menu(), "user")
    assert [a.command for a in actions] == ["cmd1", "cmd2"]


def test_get_available_actions_admin() -> None:
    actions = get_available_actions(sample_menu(), "admin")
    assert [a.command for a in actions] == ["cmd1", "cmd2", "cmd3"]


def test_count_actions_empty_submenu() -> None:
    empty = Submenu(title="Empty", items=())
    assert count_actions(empty) == 0


def test_count_actions_complex_tree() -> None:
    assert count_actions(sample_menu()) == 3


def test_render_menu_action() -> None:
    act = Action(title="Open", command="open", required_role="user")
    assert render_menu(act) == "-> [Open] (open) [user]"


def test_render_menu_separator() -> None:
    sep = Separator()
    assert render_menu(sep) == "------------------------"


def test_render_menu_nested() -> None:
    rendered = render_menu(sample_menu())
    assert "[Root]:" in rendered
    assert "[Sub]:" in rendered
    assert "-> [A1] (cmd1) [guest]" in rendered


def test_filter_menu_by_role_hierarchy() -> None:
    menu = sample_menu()
    guest_filtered = filter_menu_by_role(menu, "guest")
    assert guest_filtered is not None
    assert count_actions(guest_filtered) == 1

    admin_filtered = filter_menu_by_role(menu, "admin")
    assert admin_filtered is not None
    assert count_actions(admin_filtered) == 3


def test_filter_menu_removes_unauthorized_actions() -> None:
    act_admin = Action("Secret", "sec", required_role="admin")
    assert filter_menu_by_role(act_admin, "user") is None
    assert filter_menu_by_role(act_admin, "admin") == act_admin


def test_protocol_conformance() -> None:
    class CustomRenderable:
        def render(self, depth: int = 0) -> str:
            return "Custom"

    def print_renderable(r: CustomRenderable) -> str:
        return r.render()

    assert print_renderable(CustomRenderable()) == "Custom"


def test_pattern_matching_exhaustiveness() -> None:
    def classify(item: MenuItem) -> str:
        match item:
            case Action():
                return "action"
            case Separator():
                return "separator"
            case Submenu():
                return "submenu"

    assert classify(Action("T", "C")) == "action"
    assert classify(Separator()) == "separator"
    assert classify(Submenu("M", ())) == "submenu"


@given(st.sampled_from(["guest", "user", "admin"]))
def test_property_count_matches_admin_actions(role: Role) -> None:
    menu = sample_menu()
    actions = get_available_actions(menu, role)
    assert len(actions) <= count_actions(menu)


def test_property_role_monotonicity() -> None:
    menu = sample_menu()
    g = len(get_available_actions(menu, "guest"))
    u = len(get_available_actions(menu, "user"))
    a = len(get_available_actions(menu, "admin"))
    assert g <= u <= a


def test_immutability_of_dataclass_fields() -> None:
    sub = Submenu("Main", (Separator(),))
    with pytest.raises(FrozenInstanceError):
        sub.title = "Changed"  # type: ignore[misc]


def test_benchmark_get_actions() -> None:
    menu = sample_menu()
    t = timeit.timeit(lambda: get_available_actions(menu, "admin"), number=500)
    assert t < 0.5


def test_benchmark_render() -> None:
    menu = sample_menu()
    t = timeit.timeit(lambda: render_menu(menu), number=500)
    assert t < 0.5


def test_empty_menu_handling() -> None:
    empty = Submenu("E", ())
    assert get_available_actions(empty, "admin") == []
    assert "(порожньо)" in render_menu(empty)


def test_invalid_role_type_safety() -> None:
    assert not is_allowed("guest", "admin")
    assert is_allowed("admin", "guest")