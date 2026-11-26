"""Validation for the page-replacement module."""


def validate_reference_string(pages):
    if not pages:
        raise ValueError("Reference string is empty.")
    for p in pages:
        if not isinstance(p, int) or p < 0:
            raise ValueError(f"Invalid page number '{p}': pages must be integers >= 0.")
    return pages


def validate_frames(n):
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Number of frames must be an integer > 0.")
    return n


def parse_reference_string(text):
    """'7 0 1 2' or '7,0,1,2' -> [7, 0, 1, 2]"""
    parts = text.replace(",", " ").split()
    try:
        pages = [int(x) for x in parts]
    except ValueError:
        raise ValueError("Reference string must contain only whole numbers, e.g. 7 0 1 2 0 3")
    return validate_reference_string(pages)
