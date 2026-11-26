"""Menu for the deadlock (Banker's algorithm) module."""
import copy

from modules import deadlock
from utils.deadlock_validation import (validate_state, validate_request, parse_vector)
from utils.logger import get_logger

log = get_logger()

SAMPLE = {
    "available": [3, 3, 2],
    "maximum": [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]],
    "allocation": [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]],
}


def _print_state(state):
    need = deadlock.need_matrix(state["maximum"], state["allocation"])
    m = len(state["available"])
    res = [chr(65 + j) if m <= 26 else f"R{j}" for j in range(m)]
    print(f"\n{'':<5}{'Allocation':<16}{'Max':<16}{'Need':<16}")
    print(f"{'':<5}{' '.join(f'{r:>3}' for r in res):<16}"
          f"{' '.join(f'{r:>3}' for r in res):<16}{' '.join(f'{r:>3}' for r in res):<16}")
    for i, (al, mx, nd) in enumerate(zip(state["allocation"], state["maximum"], need)):
        fmt = lambda v: ' '.join(f'{x:>3}' for x in v)
        print(f"P{i:<4}{fmt(al):<16}{fmt(mx):<16}{fmt(nd):<16}")
    print(f"Available: {state['available']}")


def _read_matrix(label, n, m):
    rows = []
    for i in range(n):
        rows.append(parse_vector(input(f"  P{i} {label} ({m} numbers): "), m, f"{label} of P{i}"))
    return rows


def enter_state():
    try:
        n = int(input("Number of processes: "))
        m = int(input("Number of resource types: "))
    except ValueError:
        raise ValueError("Please enter whole numbers.")
    if n <= 0 or m <= 0:
        raise ValueError("Processes and resource types must be > 0.")
    available = parse_vector(input(f"Available ({m} numbers): "), m, "Available")
    maximum = _read_matrix("Max", n, m)
    allocation = _read_matrix("Allocation", n, m)
    state = {"available": available, "maximum": maximum, "allocation": allocation}
    validate_state(**state)
    return state


def safety_check(state):
    result = deadlock.is_safe(**state)
    for s in result["steps"]:
        print(f"  {s['pid']} can finish: work {s['work_before']} -> {s['work_after']}")
    if result["safe"]:
        print("\nSAFE state. Safe sequence: " + " -> ".join(result["sequence"]))
    else:
        print("\nUNSAFE state: deadlock is possible. "
              f"Processes that cannot finish: {', '.join(result['stuck'])}")
    log.info("Safety check: %s", "safe" if result["safe"] else "unsafe")


def make_request(state):
    n, m = len(state["maximum"]), len(state["available"])
    try:
        pid = int(input(f"Which process is requesting (0-{n - 1})? "))
    except ValueError:
        raise ValueError("Process number must be a whole number.")
    req = parse_vector(input(f"Request ({m} numbers): "), m, "Request")
    validate_request(pid, req, n, m)
    result = deadlock.request_resources(pid=pid, request=req, **state)
    print("\n" + result["reason"])
    if result["granted"]:
        print("Safe sequence after granting: " + " -> ".join(result["sequence"]))
        if input("Apply this request to the current state? (y/n): ").strip().lower() == "y":
            state["available"] = result["new_available"]
            state["allocation"] = result["new_allocation"]
            print("State updated.")
    log.info("Request P%d %s -> %s", pid, req,
             "granted" if result["granted"] else "denied")


_state = copy.deepcopy(SAMPLE)       # kept between visits to this menu


def deadlock_menu():
    global _state
    while True:
        print("\n--- Deadlock: Banker's Algorithm ---")
        print("1) Show current state   2) Safety check   3) Resource request")
        print("4) Enter my own state   5) Reset to sample   0) Back")
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                _print_state(_state)
            elif choice == "2":
                _print_state(_state)
                safety_check(_state)
            elif choice == "3":
                make_request(_state)
            elif choice == "4":
                _state = enter_state()
                log.info("Entered custom Banker's state")
            elif choice == "5":
                _state = copy.deepcopy(SAMPLE)
                print("State reset to the sample.")
            elif choice == "0":
                return
            else:
                print("Invalid choice.")
        except ValueError as e:
            print(f"Input error: {e}")
            log.error("Banker's validation error: %s", e)
