from collections import deque

def _result(p, start, finish):
    turnaround = finish - p["arrival"]
    return {
        "pid": p["pid"],
        "arrival": p["arrival"],
        "burst": p["burst"],
        "start": start,
        "finish": finish,
        "waiting": turnaround - p["burst"],
        "turnaround": turnaround,
        "response": start - p["arrival"],
    }


def _non_preemptive(processes, pick_key):
    """Shared engine: at each moment pick the best ready process and run it fully."""
    waiting_list = list(processes)
    time, results = 0, []
    while waiting_list:
        ready = [p for p in waiting_list if p["arrival"] <= time]
        if not ready:                       # CPU idle until the next arrival
            time = min(p["arrival"] for p in waiting_list)
            continue
        p = min(ready, key=pick_key)
        waiting_list.remove(p)
        start = time
        time += p["burst"]
        results.append(_result(p, start, time))
    return results


def fcfs(processes):
    """First Come First Served: earliest arrival goes first."""
    return _non_preemptive(processes, lambda p: (p["arrival"], p["pid"]))


def sjf(processes):
    """Shortest Job First (non-preemptive): smallest burst among ready processes."""
    return _non_preemptive(processes, lambda p: (p["burst"], p["arrival"]))


def priority(processes):
    """Priority scheduling (non-preemptive): lowest priority number first."""
    return _non_preemptive(
        processes, lambda p: (p.get("priority", 0), p["arrival"]))


def round_robin(processes, quantum=2):
    """Round Robin: each process gets at most `quantum` time units per turn."""
    procs = sorted(processes, key=lambda p: (p["arrival"], p["pid"]))
    remaining = {p["pid"]: p["burst"] for p in procs}
    first_start, finish = {}, {}
    queue, time, i, n = deque(), 0, 0, len(procs)

    def admit(now):
        nonlocal i
        while i < n and procs[i]["arrival"] <= now:
            queue.append(procs[i])
            i += 1

    while len(finish) < n:
        admit(time)
        if not queue:                       # idle: jump to next arrival
            time = procs[i]["arrival"]
            continue
        p = queue.popleft()
        pid = p["pid"]
        first_start.setdefault(pid, time)
        run = min(quantum, remaining[pid])
        time += run
        remaining[pid] -= run
        admit(time)                     
        if remaining[pid] > 0:
            queue.append(p)
        else:
            finish[pid] = time

    results = [_result(p, first_start[p["pid"]], finish[p["pid"]]) for p in procs]
    return results


def averages(results):
    """Average waiting / turnaround / response time for a result list."""
    n = len(results)
    return {
        "avg_waiting": round(sum(r["waiting"] for r in results) / n, 2),
        "avg_turnaround": round(sum(r["turnaround"] for r in results) / n, 2),
        "avg_response": round(sum(r["response"] for r in results) / n, 2),
    }
