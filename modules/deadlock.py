"""Banker's algorithm: deadlock avoidance.

State:
    available  - list, free units of each resource type
    maximum    - matrix, the most each process may ever need
    allocation - matrix, what each process currently holds
Need = Maximum - Allocation.
"""
from utils.deadlock_validation import validate_state, validate_request


def need_matrix(maximum, allocation):
    return [[mx - al for mx, al in zip(mrow, arow)]
            for mrow, arow in zip(maximum, allocation)]


def is_safe(available, maximum, allocation):
    """Safety algorithm. Returns {"safe": bool, "sequence": [pids], "steps": [...]}."""
    validate_state(available, maximum, allocation)
    need = need_matrix(maximum, allocation)
    n = len(maximum)
    work = list(available)
    finished = [False] * n
    sequence, steps = [], []

    progress = True
    while progress:
        progress = False
        for i in range(n):
            if not finished[i] and all(need[i][j] <= work[j] for j in range(len(work))):
                before = list(work)
                for j in range(len(work)):
                    work[j] += allocation[i][j]      # process finishes, releases everything
                finished[i] = True
                sequence.append(i)
                steps.append({"pid": f"P{i}", "work_before": before, "work_after": list(work)})
                progress = True
    return {"safe": all(finished), "sequence": [f"P{i}" for i in sequence],
            "steps": steps, "stuck": [f"P{i}" for i in range(n) if not finished[i]]}


def request_resources(available, maximum, allocation, pid, request):
    """Resource-request algorithm. Returns {"granted": bool, "reason": str, ...}."""
    validate_state(available, maximum, allocation)
    validate_request(pid, request, len(maximum), len(available))
    need = need_matrix(maximum, allocation)
    m = len(available)

    if any(request[j] > need[pid][j] for j in range(m)):
        return {"granted": False,
                "reason": f"P{pid} asked for more than its declared maximum need."}
    if any(request[j] > available[j] for j in range(m)):
        return {"granted": False,
                "reason": f"Not enough free resources right now; P{pid} must wait."}

    # Pretend to grant, then check if the system is still safe.
    new_available = [available[j] - request[j] for j in range(m)]
    new_alloc = [list(row) for row in allocation]
    for j in range(m):
        new_alloc[pid][j] += request[j]
    check = is_safe(new_available, maximum, new_alloc)
    if check["safe"]:
        return {"granted": True,
                "reason": "Granted: the system stays in a safe state.",
                "sequence": check["sequence"],
                "new_available": new_available, "new_allocation": new_alloc}
    return {"granted": False,
            "reason": "Denied: granting this would leave the system in an UNSAFE state."}
