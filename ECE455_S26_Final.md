# ECE455 S26 Take-Home Final Exam

## Description

Implement a Rate Monotonic (RM) single-core scheduling simulator. Report schedulability and per-task preemption counts over the first hyperperiod.

---

## Program Spec

**File:** `ece_455_final.py`  
**Run:** `python3 ece_455_final.py workload1.txt`  
**Python:** <= 3.10, stdlib only (numpy optional)  
**Time limit:** 60s per test case  
**No extra output** — strip all debug prints before submit

---

## Input Format

One task per line: `execution_time,period,relative_deadline`  
Values are positive numbers, precision up to 0.001 (floats allowed).

```
1,3,3
2,4,5
```

Tasks are numbered T0, T1, T2, ... by line order.

---

## Output Format

**Line 1:** `1` if feasible, `0` if not  
**Line 2:** If feasible → comma-separated preemption counts per task (T0,T1,...); if infeasible → blank line

### Examples

Feasible:
```
1
0,1
```

Infeasible:
```
0

```

---

## Algorithm: Rate Monotonic

- **Priority rule:** shorter period = higher priority (preemptive)
- **Simulate** the first hyperperiod (LCM of all periods)
- **Feasibility:** any deadline miss → output `0`
- **Preemption:** count each time a running task is displaced by a higher-priority task

---

## Test Cases

| Workload | Tasks | Feasible | Preemptions |
|----------|-------|----------|-------------|
| workload1.txt | T0(1,3,3), T1(2,4,5) | 1 | `0,1` |
| workload2.txt | T0(2,14,25), T1(4,16,17), T2(8,21,25), T3(5,20,30), T4(7,14,25) | 0 | *(blank)* |
| workload3.txt | T0(1,14,25), T1(3,16,17), T2(1,21,25), T3(2,20,30), T4(1,14,25) | 1 | `0,15,0,3,0` |
| workload4.txt | T0(2,4,6), T1(1.5,8,10), T2(1.5,8,9), T3(1,8,15) | 1 | `0,0,1,0` |
| workload5.txt | T0(1,4,2), T1(3,6,10), T2(1,8,9), T3(1,12,12) | 1 | `0,2,0,0` |
| workload6.txt | T0(2,4,6), T1(1.5,8,10), T2(1.5,8,9), T3(1,8,15), T4(1.5,16,20) | 0 | *(blank)* |

---

## Key Implementation Notes

### Floating Point
Periods/deadlines/exec times can be floats (0.001 precision). Multiply all values by **1000** and work in integer time units to avoid floating-point LCM issues.

### Hyperperiod
`hyperperiod = LCM(P0, P1, ..., Pn)` — simulate from t=0 to t=hyperperiod.

### Simulation Approach (Event-Driven)
Events: task releases (`k * Pi` for each job k) and task completions.  
At each event:
1. Release new jobs whose release time has arrived
2. Check deadline misses among active jobs
3. If current running task preempted by higher-priority ready task → increment preemption count
4. Run highest-priority ready task until next event

### Preemption Definition
Task Ti is preempted when it is **currently executing** and a newly released task Tj with **higher RM priority** (shorter period) becomes ready, causing Ti to stop.

### Deliverable
Zip containing Git repo (with `.git/`) + `ece_455_final.py` at top level → submit to Learn dropbox.
