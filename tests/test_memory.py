import unittest
from modules.memory import fifo, lru, optimal
from modules.memory_cli import SAMPLE, BELADY
from utils.memory_validation import (validate_reference_string, validate_frames,
                                     parse_reference_string)


class TestKnownResults(unittest.TestCase):
    """Textbook reference string, 3 frames: FIFO 15, LRU 12, Optimal 9 faults."""
    def test_fifo(self):
        self.assertEqual(fifo(SAMPLE, 3)["faults"], 15)

    def test_lru(self):
        self.assertEqual(lru(SAMPLE, 3)["faults"], 12)

    def test_optimal(self):
        self.assertEqual(optimal(SAMPLE, 3)["faults"], 9)

    def test_optimal_never_worse(self):
        self.assertLessEqual(optimal(SAMPLE, 3)["faults"], lru(SAMPLE, 3)["faults"])
        self.assertLessEqual(optimal(SAMPLE, 3)["faults"], fifo(SAMPLE, 3)["faults"])

    def test_belady_anomaly(self):
        self.assertEqual(fifo(BELADY, 3)["faults"], 9)
        self.assertEqual(fifo(BELADY, 4)["faults"], 10)


class TestBoundary(unittest.TestCase):
    def test_one_frame_every_change_faults(self):
        self.assertEqual(fifo([1, 2, 1, 2], 1)["faults"], 4)

    def test_same_page_repeated(self):
        r = lru([5, 5, 5, 5], 2)
        self.assertEqual(r["faults"], 1)
        self.assertEqual(r["hits"], 3)

    def test_more_frames_than_pages(self):
        self.assertEqual(optimal([1, 2, 3], 10)["faults"], 3)


class TestInvalid(unittest.TestCase):
    def test_empty_string(self):
        with self.assertRaises(ValueError):
            validate_reference_string([])

    def test_negative_page(self):
        with self.assertRaises(ValueError):
            validate_reference_string([1, -2, 3])

    def test_zero_frames(self):
        with self.assertRaises(ValueError):
            fifo([1, 2, 3], 0)

    def test_non_numeric_input(self):
        with self.assertRaises(ValueError):
            parse_reference_string("1 two 3")

    def test_parse_commas(self):
        self.assertEqual(parse_reference_string("7,0, 1"), [7, 0, 1])


if __name__ == "__main__":
    unittest.main()
