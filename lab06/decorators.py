"""Параметризовані декоратори як функції вищого порядку (HOF)."""

from __future__ import annotations

import functools
import random
import threading
import time
from typing import Any, Callable, Hashable, Literal, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def make_key(args: tuple[Any, ...], kwargs: dict[str, Any]) -> Hashable:
    """Генерація хешованого ключа з args та kwargs."""
    return (args, tuple(sorted(kwargs.items())))


def timed(
    label: str | None = None,
    *,
    unit: Literal["s", "ms", "us"] = "ms",
    logger: Callable[[str], None] = print,
    clock: Callable[[], float] = time.perf_counter,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Декоратор вимірювання часу виконання функції з гарантією логування у finally."""
    factor = {"s": 1.0, "ms": 1e3, "us": 1e6}[unit]

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        name = label or func.__name__

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            t0 = clock()
            try:
                return func(*args, **kwargs)
            finally:
                dt = (clock() - t0) * factor
                logger(f"[timed] {name} took {dt:.3f} {unit}")

        return wrapper

    return decorator


def retries(
    attempts: int = 3,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
    delay: float = 0.0,
    backoff: float = 1.0,
    jitter: float = 0.0,
    *,
    sleep: Callable[[float], None] = time.sleep,
    logger: Callable[[str], None] = lambda _: None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Декоратор повторних спроб виконання з експоненційним бекофом."""
    if attempts < 1:
        raise ValueError("attempts must be >= 1")

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            exc: BaseException | None = None
            for i in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    exc = e
                    if i == attempts:
                        logger(f"[retries] fail after {i} attempts: {e!r}")
                        break
                    wait = delay * (backoff ** (i - 1)) + (
                        random.random() * jitter if jitter else 0.0
                    )
                    logger(f"[retries] attempt {i} failed: {e!r}; sleeping {wait:.3f}s")
                    sleep(wait)
            assert exc is not None
            raise exc

        return wrapper

    return decorator


def cached(
    *,
    ttl: float | None = None,
    time_fn: Callable[[], float] = time.time,
) -> Callable[[Callable[P, R]], Any]:
    """Потокобезпечний кеш з підтримкою TTL, точкової інвалідації та статистики hit/miss."""

    def decorator(func: Callable[P, R]) -> Any:
        cache: dict[Hashable, tuple[float | None, R]] = {}
        lock = threading.Lock()
        stats = {"hits": 0, "misses": 0}

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = make_key(args, kwargs)
            now = time_fn()

            with lock:
                if key in cache:
                    exp, val = cache[key]
                    if exp is None or now < exp:
                        stats["hits"] += 1
                        return val
                    del cache[key]
                stats["misses"] += 1

            val = func(*args, **kwargs)

            with lock:
                expiry = None if ttl is None else now + ttl
                cache[key] = (expiry, val)
            return val

        def cache_clear() -> None:
            with lock:
                cache.clear()
                stats["hits"] = 0
                stats["misses"] = 0

        def cache_invalidate(
            predicate: Callable[[tuple[Any, ...], dict[str, Any]], bool]
        ) -> int:
            removed = 0
            with lock:
                for k in list(cache.keys()):
                    args_k = k[0]
                    kwargs_k = dict(k[1])
                    if predicate(args_k, kwargs_k):
                        del cache[k]
                        removed += 1
            return removed

        wrapper.cache_clear = cache_clear
        wrapper.cache_invalidate = cache_invalidate
        wrapper.cache_info = lambda: stats.copy()
        return wrapper

    return decorator


def count_calls() -> Callable[[Callable[P, R]], Any]:
    """Декоратор обліку кількості викликів (Варіант 12)."""

    def decorator(func: Callable[P, R]) -> Any:
        count = 0

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            nonlocal count
            count += 1
            return func(*args, **kwargs)

        def _reset() -> None:
            nonlocal count
            count = 0

        wrapper.calls = lambda: count
        wrapper.reset = _reset
        return wrapper

    return decorator