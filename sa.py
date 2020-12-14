from copy import copy
from random import seed, shuffle
import sys
import math
import random
from itertools import combinations, product

STABILIZED_NONCOVERAGE_CNT = 0
INITIAL_TEMP = 10
_count_noncoverage_cache = set()


def initial_state(t, k, v, n):
    return [[random.choice(v[j]) for j in range(k)] for _ in range(n)]


def stabilized(cnt, temp):
    return cnt <= STABILIZED_NONCOVERAGE_CNT or temp <= -2*INITIAL_TEMP


def count_noncoverage(a, t, v, flush=False):
    if flush:
        for comb in combinations(range(len(v)), t):
            for elem in product(*[v[i] for i in comb]):
                _count_noncoverage_cache.update([tuple(zip(comb, elem))])
    cover_pairs = []
    for cover in a:
        for comb in combinations(range(len(cover)), t):
            values = tuple((i, cover[i]) for i in comb)
            cover_pairs.append(values)
    return len(_count_noncoverage_cache - set(cover_pairs))


def cool(temp):
    return temp - .05


# t: strength
# k: number of configs
# v: v[i] contains array of i-th config's possible values (1<=i<=k)
# n: size of covering aray
# a: covering arrays; a[i][j] == value of j-th config of i-th covering
def anneal(t, k, v, n):
    print(f'annealing started (n={n}, t={t}, k={k})')
    a = initial_state(t, k, v, n)
    temp = INITIAL_TEMP
    step = 0
    while not stabilized(count_noncoverage(a, t, v), temp):
        row = random.choice(range(n))
        col = random.choice(range(k))
        symbol = random.choice(v[col])
        aa = [[e for e in row] for row in a]
        aa[row][col] = symbol
        fitness_diff = count_noncoverage(aa, t, v) - count_noncoverage(a, t, v)
        if fitness_diff <= 0:
            a = aa
        else:
            prob = math.sqrt(math.exp(-fitness_diff / max(1, temp)) / 10)
            if temp <= 0:
                prob = 0
            if random.random() < prob:
                a = aa
        if step % (100 if t == 2 else 1) == 0:
            print(f'  step: {step}, temp: {temp}, fitness: {count_noncoverage(a, t, v)}')
        step += 1
        temp = cool(temp)
    return a


def binary_search(t, k, v, lower, upper):
    a = []
    n = (lower + 2 * upper) // 3
    count_noncoverage([], t, v, flush=True)
    while upper >= lower:
        aa = anneal(t, k, v, n)
        if count_noncoverage(aa, t, v) == 0:
            a = aa
            upper = n-1
        else:
            lower = n+1
        n = (lower + 2 * upper) // 3
    return a


def cit(filename, t=2, lower=5, upper=100):
    v_tags = []
    v = []
    with open(filename, "r") as f:
        for line in f:
            text = line.strip()
            if not text:
                continue
            param_name, param_values = text.split(":")
            param_name = param_name.strip()
            param_values = param_values.split()
            v_tags.append(param_name)
            v.append(param_values)
    k = len(v)
    ca = binary_search(t, k, v, lower, upper)
    return ca

if __name__ == '__main__':
    from pprint import pprint
    res = cit("input.txt")
    print(res)
    a = 0
    for test in res:
        a += 1
        print(f"Test #{a}")
        print("-"*len(f"Test #{a}"))
        pprint(test)
        print()
