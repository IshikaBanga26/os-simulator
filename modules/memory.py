"""Page replacement algorithms: FIFO, LRU, Optimal.

Each function takes a reference string (list of page numbers) and a number
of frames, and returns:
    {"faults": int, "hits": int, "hit_ratio": float, "steps": [...]}
where each step is {"page": p, "frames": [...], "fault": bool}.
"""
from collections import deque
from utils.memory_validation import validate_reference_string, validate_frames


def _summary(pages, steps):
    faults = sum(1 for s in steps if s["fault"])
    hits = len(pages) - faults
    return {"faults": faults, "hits": hits,
            "hit_ratio": round(hits / len(pages), 2), "steps": steps}


def fifo(pages, n_frames):
    """Evict the page that has been in memory the longest."""
    validate_reference_string(pages)
    validate_frames(n_frames)
    frames, steps = deque(), []
    for p in pages:
        fault = p not in frames
        if fault:
            if len(frames) == n_frames:
                frames.popleft()
            frames.append(p)
        steps.append({"page": p, "frames": list(frames), "fault": fault})
    return _summary(pages, steps)


def lru(pages, n_frames):
    """Evict the page that was used least recently."""
    validate_reference_string(pages)
    validate_frames(n_frames)
    frames, steps = [], []          # front = least recently used
    for p in pages:
        fault = p not in frames
        if fault:
            if len(frames) == n_frames:
                frames.pop(0)
        else:
            frames.remove(p)        # refresh: move to most-recent end
        frames.append(p)
        steps.append({"page": p, "frames": list(frames), "fault": fault})
    return _summary(pages, steps)


def optimal(pages, n_frames):
    """Evict the page whose next use is farthest in the future (needs the whole string)."""
    validate_reference_string(pages)
    validate_frames(n_frames)
    frames, steps = [], []
    for i, p in enumerate(pages):
        fault = p not in frames
        if fault:
            if len(frames) == n_frames:
                future = pages[i + 1:]
                def next_use(x):
                    return future.index(x) if x in future else float("inf")
                frames.remove(max(frames, key=next_use))
            frames.append(p)
        steps.append({"page": p, "frames": list(frames), "fault": fault})
    return _summary(pages, steps)


ALGORITHMS = {"FIFO": fifo, "LRU": lru, "Optimal": optimal}
