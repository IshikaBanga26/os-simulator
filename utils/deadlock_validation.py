"""Validation for the deadlock (Banker's algorithm) module."""


def _check_vector(vec, length, label):
    if not isinstance(vec, list) or len(vec) != length:
        raise ValueError(f"{label} must have exactly {length} values.")
    for v in vec:
        if not isinstance(v, int) or v < 0:
            raise ValueError(f"{label} must contain integers >= 0 (got {v}).")


def validate_state(available, maximum, allocation):
    if not maximum or not allocation:
        raise ValueError("Max and Allocation matrices cannot be empty.")
    if not available:
        raise ValueError("Available vector cannot be empty.")
    m = len(available)
    _check_vector(available, m, "Available")
    if len(maximum) != len(allocation):
        raise ValueError("Max and Allocation must have the same number of processes.")
    for i, (mx, al) in enumerate(zip(maximum, allocation)):
        _check_vector(mx, m, f"Max of P{i}")
        _check_vector(al, m, f"Allocation of P{i}")
        for j in range(m):
            if al[j] > mx[j]:
                raise ValueError(
                    f"P{i}: allocation ({al[j]}) cannot exceed max ({mx[j]}) for resource {j}.")


def validate_request(pid, request, n_processes, n_resources):
    if not isinstance(pid, int) or not 0 <= pid < n_processes:
        raise ValueError(f"Process number must be between 0 and {n_processes - 1}.")
    _check_vector(request, n_resources, "Request")


def parse_vector(text, length, label="Vector"):
    try:
        vec = [int(x) for x in text.replace(",", " ").split()]
    except ValueError:
        raise ValueError(f"{label} must contain only whole numbers.")
    _check_vector(vec, length, label)
    return vec
