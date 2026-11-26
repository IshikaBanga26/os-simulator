"""Plain-text tables for results."""


def print_results(title, results):
    print(f"\n=== {title} ===")
    header = f"{'PID':<6}{'Arr':>5}{'Burst':>7}{'Finish':>8}{'Wait':>6}{'TAT':>6}{'Resp':>6}"
    print(header)
    print("-" * len(header))
    for r in sorted(results, key=lambda r: r["pid"]):
        print(f"{r['pid']:<6}{r['arrival']:>5}{r['burst']:>7}{r['finish']:>8}"
              f"{r['waiting']:>6}{r['turnaround']:>6}{r['response']:>6}")


def print_comparison(summary):
    """summary = {"FCFS": {"avg_waiting":..,...}, ...}"""
    print("\n=== Algorithm comparison (averages) ===")
    header = f"{'Algorithm':<14}{'Avg Wait':>10}{'Avg TAT':>10}{'Avg Resp':>10}"
    print(header)
    print("-" * len(header))
    for name, a in summary.items():
        print(f"{name:<14}{a['avg_waiting']:>10}{a['avg_turnaround']:>10}{a['avg_response']:>10}")
    best = min(summary, key=lambda k: summary[k]["avg_waiting"])
    print(f"\nBest by average waiting time: {best}")
