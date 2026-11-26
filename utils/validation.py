"""Input validation. Every function raises ValueError with a clear message."""


def validate_processes(processes):
    if not processes:
        raise ValueError("Process list is empty.")
    seen = set()
    for p in processes:
        for key in ("pid", "arrival", "burst"):
            if key not in p:
                raise ValueError(f"Process missing field '{key}': {p}")
        pid = p["pid"]
        if pid in seen:
            raise ValueError(f"Duplicate process id: {pid}")
        seen.add(pid)
        if not isinstance(p["arrival"], int) or p["arrival"] < 0:
            raise ValueError(f"{pid}: arrival time must be an integer >= 0.")
        if not isinstance(p["burst"], int) or p["burst"] <= 0:
            raise ValueError(f"{pid}: burst time must be an integer > 0.")
        if not isinstance(p.get("priority", 0), int):
            raise ValueError(f"{pid}: priority must be an integer.")
    return processes


def validate_quantum(q):
    if not isinstance(q, int) or q <= 0:
        raise ValueError("Time quantum must be an integer > 0.")
    return q
