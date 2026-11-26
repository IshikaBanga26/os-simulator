"""Menu for the page-replacement module."""
from modules.memory import ALGORITHMS, fifo
from utils.memory_validation import parse_reference_string, validate_frames
from utils.logger import get_logger

log = get_logger()
SAMPLE = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
BELADY = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]


def _ask_inputs():
    raw = input("Reference string (blank = sample): ").strip()
    pages = parse_reference_string(raw) if raw else SAMPLE
    raw = input("Number of frames [3]: ").strip() or "3"
    try:
        frames = validate_frames(int(raw))
    except ValueError:
        raise ValueError("Number of frames must be an integer > 0.")
    return pages, frames


def _print_trace(name, pages, result):
    print(f"\n=== {name} ===")
    print(f"{'Page':<6}{'Frames':<20}Result")
    print("-" * 34)
    for s in result["steps"]:
        print(f"{s['page']:<6}{str(s['frames']):<20}{'FAULT' if s['fault'] else 'hit'}")
    print(f"Faults: {result['faults']}  Hits: {result['hits']}  "
          f"Hit ratio: {result['hit_ratio']}")


def _print_comparison(results):
    print("\n=== Page replacement comparison ===")
    header = f"{'Algorithm':<12}{'Faults':>8}{'Hits':>7}{'Hit ratio':>11}"
    print(header)
    print("-" * len(header))
    for name, r in results.items():
        print(f"{name:<12}{r['faults']:>8}{r['hits']:>7}{r['hit_ratio']:>11}")
    best = min(results, key=lambda k: results[k]["faults"])
    print(f"\nFewest page faults: {best}")


def belady_demo():
    print("\nBelady's anomaly: with FIFO, MORE frames can cause MORE faults.")
    print(f"Reference string: {BELADY}")
    for n in (3, 4):
        r = fifo(BELADY, n)
        print(f"  FIFO with {n} frames -> {r['faults']} faults")
    log.info("Ran Belady's anomaly demo")


def memory_menu():
    print("\n1) FIFO  2) LRU  3) Optimal  4) Compare all  5) Belady's anomaly demo  0) Back")
    choice = input("Choose: ").strip()
    if choice == "0":
        return
    if choice == "5":
        belady_demo()
        return
    if choice not in ("1", "2", "3", "4"):
        print("Invalid choice.")
        return
    pages, frames = _ask_inputs()
    names = list(ALGORITHMS)
    if choice == "4":
        results = {n: ALGORITHMS[n](pages, frames) for n in names}
        _print_comparison(results)
        log.info("Compared page replacement algorithms (%d pages, %d frames)",
                 len(pages), frames)
    else:
        name = names[int(choice) - 1]
        result = ALGORITHMS[name](pages, frames)
        _print_trace(name, pages, result)
        log.info("Ran %s (%d pages, %d frames)", name, len(pages), frames)
