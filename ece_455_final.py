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


def simulate(tasks_int, priority, hyperperiod):
    n = len(tasks_int)
    preemptions = [0] * n
    # active_jobs: list of [task_idx, remaining_exec, absolute_deadline]
    active_jobs = []
    t = 0

    # precompute all release times for each task within hyperperiod
    # release_times[i] = sorted list of release times for task i
    release_schedule = {}
    for i, (e, p, d) in enumerate(tasks_int):
        releases = list(range(0, hyperperiod, p))
        release_schedule[i] = releases

    # next_release_idx[i] = index into release_schedule[i] of next unreleased job
    next_release_idx = [0] * n

    current_task = None   # index of currently running task
    current_remaining = 0

    while t < hyperperiod:
        # release all jobs due at time t
        for i in range(n):
            idx = next_release_idx[i]
            releases = release_schedule[i]
            while idx < len(releases) and releases[idx] == t:
                e, p, d = tasks_int[i]
                active_jobs.append([i, e, t + d])
                idx += 1
            next_release_idx[i] = idx

        # check deadline misses: any active job whose deadline <= t
        for job in active_jobs:
            if job[2] <= t:
                return None, None  # infeasible

        # find highest priority ready job (lowest priority rank)
        if not active_jobs:
            # CPU idle — advance to next release
            next_releases = []
            for i in range(n):
                idx = next_release_idx[i]
                releases = release_schedule[i]
                if idx < len(releases):
                    next_releases.append(releases[idx])
            if not next_releases:
                break
            t = min(next_releases)
            current_task = None
            current_remaining = 0
            continue

        best = min(active_jobs, key=lambda j: (priority[j[0]], j[0]))
        best_task = best[0]

        # check if preemption occurs
        if current_task is not None and current_task != best_task:
            preemptions[current_task] += 1

        current_task = best_task
        current_remaining = best[1]

        # find time of next event after t
        next_events = []

        # next job releases
        for i in range(n):
            idx = next_release_idx[i]
            releases = release_schedule[i]
            if idx < len(releases):
                next_events.append(releases[idx])

        # current job completion
        next_events.append(t + current_remaining)

        # nearest active job deadline
        for job in active_jobs:
            if job[2] > t:
                next_events.append(job[2])

        next_t = min(e for e in next_events if e > t)
        elapsed = next_t - t

        # advance all active jobs' remaining time for current running job
        best[1] -= elapsed
        t = next_t

        # remove completed job
        if best[1] <= 0:
            active_jobs.remove(best)
            current_task = None
            current_remaining = 0

    # after hyperperiod: check any unfinished jobs
    if active_jobs:
        return None, None  # infeasible

    return True, preemptions


def main():
    if len(sys.argv) != 2:
        sys.exit(1)
    filename = sys.argv[1]
    tasks = parse_tasks(filename)
    tasks_int = scale_tasks(tasks)
    priority = assign_priorities(tasks_int)
    hyperperiod = compute_hyperperiod(tasks_int)
    feasible, preemptions = simulate(tasks_int, priority, hyperperiod)
    if not feasible:
        print(0)
        print()
    else:
        print(1)
        print(','.join(str(p) for p in preemptions))


if __name__ == "__main__":
    main()

