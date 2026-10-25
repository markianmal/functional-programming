"""Тести базових алгоритмів."""

from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st
import pytest
from algorithms import (
    Node,
    bfs_level_order,
    dfs_preorder_iter,
    fib,
    fib_iter,
    fib_naive,
    height,
    inorder,
    postorder,
    preorder,
    quicksort,
)


def test_fib_parity() -> None:
    for n in range(20):
        assert fib(n) == fib_naive(n) == fib_iter(n)


def test_fib_negative() -> None:
    with pytest.raises(ValueError):
        fib(-1)


def test_tree_traversals() -> None:
    t = Node(4, Node(2, Node(1), Node(3)), Node(6, None, Node(7)))
    assert list(preorder(t)) == [4, 2, 1, 3, 6, 7]
    assert list(inorder(t)) == [1, 2, 3, 4, 6, 7]
    assert list(postorder(t)) == [1, 3, 2, 7, 6, 4]
    assert bfs_level_order(t) == [4, 2, 6, 1, 3, 7]
    assert dfs_preorder_iter(t) == [4, 2, 1, 3, 6, 7]
    assert height(t) == 3


@given(st.lists(st.integers()))
def test_quicksort_property(xs: list[int]) -> None:
    assert quicksort(xs) == sorted(xs)