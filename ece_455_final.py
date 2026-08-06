import sys
from math import gcd
from functools import reduce


def parse_tasks(filename):
    tasks = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line:
                e, p, d = [float(x) for x in line.split(',')]
                tasks.append((e, p, d))
    return tasks


SCALE = 1000


def lcm(a, b):
    return a * b // gcd(a, b)


def scale_tasks(tasks):
    return [(round(e * SCALE), round(p * SCALE), round(d * SCALE)) for e, p, d in tasks]


def assign_priorities(tasks_int):
    # RM: shorter period = higher priority (lower rank number)
    # tie-break by original task index for determinism
    order = sorted(range(len(tasks_int)), key=lambda i: (tasks_int[i][1], i))
    priority = [0] * len(tasks_int)
    for rank, i in enumerate(order):
        priority[i] = rank
    return priority


def compute_hyperperiod(tasks_int):
    return reduce(lcm, [p for _, p, _ in tasks_int])


def main():
    if len(sys.argv) != 2:
        sys.exit(1)
    filename = sys.argv[1]
    tasks = parse_tasks(filename)
    tasks_int = scale_tasks(tasks)
    priority = assign_priorities(tasks_int)
    hyperperiod = compute_hyperperiod(tasks_int)


if __name__ == "__main__":
    main()

