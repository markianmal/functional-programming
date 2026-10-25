"""Скрипт заміру продуктивності: наївна vs мемоізована vs ітеративна версія."""

import time
from lcs import lcs_iterative, lcs_memo, lcs_naive


def benchmark() -> None:
    s1_short = "AGGTAB1234"
    s2_short = "GXTXAYB123"

    print("=== Порівняння наївного та оптимізованого підходів ===")
    t0 = time.perf_counter()
    res_naive = lcs_naive(s1_short, s2_short)
    t1 = time.perf_counter()
    naive_time = t1 - t0
    print(f"lcs_naive:     res={res_naive}, час: {naive_time:.6f} сек")

    t0 = time.perf_counter()
    res_memo = lcs_memo(s1_short, s2_short)
    t1 = time.perf_counter()
    memo_time = t1 - t0
    print(f"lcs_memo:      res={res_memo}, час: {memo_time:.6f} сек")

    t0 = time.perf_counter()
    res_iter = lcs_iterative(s1_short, s2_short)
    t1 = time.perf_counter()
    iter_time = t1 - t0
    print(f"lcs_iterative: res={res_iter}, час: {iter_time:.6f} сек")

    if memo_time > 0:
        print(f"Прискорення мемоізації: {naive_time / memo_time:.2f}x\n")

    print("=== Довгі рядки (наївний підхід заблоковано через експоненту) ===")
    s1_long = "ALGORITHM_DESIGN_TECHNIQUES" * 4
    s2_long = "DYNAMIC_PROGRAMMING_APPROACH" * 4

    t0 = time.perf_counter()
    res_memo_l = lcs_memo(s1_long, s2_long)
    t1 = time.perf_counter()
    print(f"lcs_memo (довгий):      res={res_memo_l}, час: {t1 - t0:.6f} сек")

    t0 = time.perf_counter()
    res_iter_l = lcs_iterative(s1_long, s2_long)
    t1 = time.perf_counter()
    print(f"lcs_iterative (довгий): res={res_iter_l}, час: {t1 - t0:.6f} сек")


if __name__ == "__main__":
    benchmark()