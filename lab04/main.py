from __future__ import annotations
import sys
import timeit
from algorithms import Node, bfs_level_order, fib, fib_iter, fib_naive, inorder, quicksort
from lcs import _lcs_memo_rec, lcs_len, lcs_len_naive, lcs_string

def main() -> None:
    print("=== Демонстрація Варіанта 12 (LCS) ===")
    s1, s2 = "AGGTAB", "GXTXAYB"
    print(f"lcs_string('{s1}', '{s2}') -> '{lcs_string(s1, s2)}' (довжина {lcs_len(s1, s2)})")

    s1_bench, s2_bench = "AGGTAB1234", "GXTXAYB123"
    _lcs_memo_rec.cache_clear()
    t_cached = timeit.timeit(lambda: lcs_len(s1_bench, s2_bench), number=1)
    t_naive = timeit.timeit(lambda: lcs_len_naive(s1_bench, s2_bench), number=1)
    print(f"lcs_len('{s1_bench}', '{s2_bench}') cached: {t_cached * 1e3:.3f} ms")
    print(f"lcs_len_naive('{s1_bench}', '{s2_bench}'): {t_naive * 1e3:.3f} ms")
    if t_cached > 0:
        print(f"Прискорення за рахунок мемоізації: {t_naive / t_cached:.1f}x")
    print("cache_info:", _lcs_memo_rec.cache_info())

    print("\n=== Базові алгоритми ===")
    fib.cache_clear()
    t_fib_c = timeit.timeit(lambda: fib(30), number=1)
    t_fib_n = timeit.timeit(lambda: fib_naive(30), number=1)
    print(f"fib(30) cached: {t_fib_c * 1e3:.3f} ms")
    print(f"fib(30) naive: {t_fib_n * 1e3:.3f} ms")
    print(f"fib(90) result: {fib(90)} | fib_iter(90): {fib_iter(90)}")
    print("Quicksort test:", quicksort([3, 1, 4, 1, 5, 9, 2, 6]))

    t = Node(4, Node(2, Node(1), Node(3)), Node(6, None, Node(7)))
    print("Tree Inorder:", list(inorder(t)), "| BFS:", bfs_level_order(t))
    print("CPython recursion limit:", sys.getrecursionlimit())

if __name__ == "__main__":
    main()