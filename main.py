"""OS Resource-Management Simulator"""
import json
import shutil
import subprocess
from pathlib import Path

from modules import scheduler
from utils.logger import get_logger
from utils.report import print_results, print_comparison
from utils.validation import validate_processes, validate_quantum

BASE = Path(__file__).resolve().parent
SAMPLE = BASE / "data" / "sample_processes.json"
log = get_logger()


def load_sample():
    with open(SAMPLE) as f:
        return validate_processes(json.load(f))


def enter_processes():
    """Type processes by hand: 'pid arrival burst priority' per line, blank line to finish."""
    print("Enter: pid arrival burst priority   (blank line to finish)")
    procs = []
    while True:
        line = input("> ").strip()
        if not line:
            break
        try:
            pid, arr, burst, prio = line.split()
            procs.append({"pid": pid, "arrival": int(arr),
                          "burst": int(burst), "priority": int(prio)})
        except ValueError:
            print("  Invalid line. Example: P1 0 5 2")
    return validate_processes(procs)


def ask_quantum():
    raw = input("Time quantum for Round Robin [2]: ").strip() or "2"
    try:
        return validate_quantum(int(raw))
    except ValueError:
        raise ValueError("Time quantum must be an integer > 0.")


def run_all(processes, quantum):
    return {
        "FCFS": scheduler.fcfs(processes),
        "SJF": scheduler.sjf(processes),
        "Priority": scheduler.priority(processes),
        f"RR (q={quantum})": scheduler.round_robin(processes, quantum),
    }


def scheduling_menu(processes):
    print("\n1) FCFS  2) SJF  3) Priority  4) Round Robin  5) Compare all  0) Back")
    choice = input("Choose: ").strip()
    if choice == "0":
        return
    quantum = ask_quantum() if choice in ("4", "5") else 2
    runs = run_all(processes, quantum)
    names = list(runs)
    if choice in ("1", "2", "3", "4"):
        name = names[int(choice) - 1]
        print_results(name, runs[name])
        log.info("Ran %s on %d processes", name, len(processes))
    elif choice == "5":
        for name, res in runs.items():
            print_results(name, res)
        print_comparison({n: scheduler.averages(r) for n, r in runs.items()})
        log.info("Compared all scheduling algorithms")
    else:
        print("Invalid choice.")

def show_system_info():
    if shutil.which("bash") is None:
        print("Bash not found. Run this on Linux/WSL to see real system info.")
        return
    result = subprocess.run(
        ["bash", str(BASE / "scripts" / "system_info.sh")],
        capture_output=True, text=True)
    print(result.stdout or result.stderr)


def main():
    processes = load_sample()
    log.info("Simulator started")
    while True:
        print("\n===== OS SIMULATOR =====")
        print("1) CPU Scheduling")
        print("2) Enter my own processes")
        print("3) Show current processes")
        print("4) Show real system info (Bash)")
        print("0) Exit")
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                scheduling_menu(processes)
            elif choice == "2":
                processes = enter_processes()
            elif choice == "3":
                for p in processes:
                    print(p)
            elif choice == "4":
                show_system_info()
                log.info("Displayed system info")
            elif choice == "0":
                log.info("Simulator exited")
                break
            else:
                print("Invalid choice, try again.")
        except ValueError as e:
            print(f"Input error: {e}")
            log.error("Validation error: %s", e)
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break


if __name__ == "__main__":
    main()
