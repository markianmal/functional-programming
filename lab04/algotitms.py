"""Базові рекурсивні та ітеративні алгоритми ЛР4."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from functools import lru_cache
from random import choice
from typing import Iterator


def quicksort(xs: list[int]) -> list[int]:
    """Рекурсивний quicksort із випадковим pivot та переходом на insertion sort."""
    if len(xs) <= 1:
        return xs[:]

    if len(xs) < 32:
        arr = xs[:]
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

    p = choice(xs)
    left = [x for x in xs if x < p]
    mid = [x for x in xs if x == p]
    right = [x for x in xs if x > p]
    return quicksort(left) + mid + quicksort(right)


@dataclass(frozen=True, slots=True)
class Node:
    """Незмінний вузол бінарного дерева."""

    key: int
    left: Node | None = None
    right: Node | None = None


def preorder(t: Node | None) -> Iterator[int]:
    if t is None:
        return
    yield t.key
    yield from preorder(t.left)
    yield from preorder(t.right)


def inorder(t: Node | None) -> Iterator[int]:
    if t is None:
        return
    yield from inorder(t.left)
    yield t.key
    yield from inorder(t.right)


def postorder(t: Node | None) -> Iterator[int]:
    if t is None:
        return
    yield from postorder(t.left)
    yield from postorder(t.right)
    yield t.key


def bfs_level_order(t: Node | None) -> list[int]:
    """Ітеративний BFS через deque, безпечний до глибини дерева."""
    if not t:
        return []
    q: deque[Node] = deque([t])
    out: list[int] = []
    while q:
        n = q.popleft()
        out.append(n.key)
        if n.left:
            q.append(n.left)
        if n.right:
            q.append(n.right)
    return out


def dfs_preorder_iter(t: Node | None) -> list[int]:
    """Ітеративний DFS через власний стек у купі."""
    if not t:
        return []
    stack: list[Node] = [t]
    out: list[int] = []
    while stack:
        n = stack.pop()
        out.append(n.key)
        if n.right:
            stack.append(n.right)
        if n.left:
            stack.append(n.left)
    return out


def height(t: Node | None) -> int:
    return 0 if t is None else 1 + max(height(t.left), height(t.right))


@lru_cache(maxsize=100_000)
def fib(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    return n if n < 2 else fib(n - 1) + fib(n - 2)


def fib_naive(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    return n if n < 2 else fib_naive(n - 1) + fib_naive(n - 2)


def fib_iter(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a