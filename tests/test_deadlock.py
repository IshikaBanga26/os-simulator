import unittest
from modules import deadlock
from modules.deadlock_cli import SAMPLE
from utils.deadlock_validation import validate_state, parse_vector


class TestSafety(unittest.TestCase):
    def test_textbook_sample_is_safe(self):
        r = deadlock.is_safe(**SAMPLE)
        self.assertTrue(r["safe"])
        self.assertEqual(r["sequence"], ["P1", "P3", "P4", "P0", "P2"])

    def test_need_matrix(self):
        need = deadlock.need_matrix(SAMPLE["maximum"], SAMPLE["allocation"])
        self.assertEqual(need[0], [7, 4, 3])
        self.assertEqual(need[1], [1, 2, 2])

    def test_unsafe_state(self):
        # Two processes each holding 1 unit and needing 1 more; nothing free.
        r = deadlock.is_safe([0], [[2], [2]], [[1], [1]])
        self.assertFalse(r["safe"])
        self.assertEqual(r["stuck"], ["P0", "P1"])


class TestRequests(unittest.TestCase):
    def test_safe_request_granted(self):
        r = deadlock.request_resources(pid=1, request=[1, 0, 2], **SAMPLE)
        self.assertTrue(r["granted"])

    def test_request_exceeds_need(self):
        r = deadlock.request_resources(pid=1, request=[9, 9, 9], **SAMPLE)
        self.assertFalse(r["granted"])
        self.assertIn("maximum", r["reason"])

    def test_request_exceeds_available(self):
        r = deadlock.request_resources(pid=0, request=[7, 0, 0], **SAMPLE)
        self.assertFalse(r["granted"])
        self.assertIn("wait", r["reason"])

    def test_unsafe_request_denied(self):
        # After granting P1 (1,0,2), P4 asking (3,3,0) would be unsafe.
        first = deadlock.request_resources(pid=1, request=[1, 0, 2], **SAMPLE)
        state = {"available": first["new_available"], "maximum": SAMPLE["maximum"],
                 "allocation": first["new_allocation"]}
        r = deadlock.request_resources(pid=4, request=[3, 3, 0], **state)
        self.assertFalse(r["granted"])

    def test_zero_request_is_fine(self):
        self.assertTrue(deadlock.request_resources(pid=0, request=[0, 0, 0], **SAMPLE)["granted"])


class TestInvalid(unittest.TestCase):
    def test_empty_matrices(self):
        with self.assertRaises(ValueError):
            validate_state([1], [], [])

    def test_allocation_exceeds_max(self):
        with self.assertRaises(ValueError):
            validate_state([1], [[2]], [[3]])

    def test_negative_available(self):
        with self.assertRaises(ValueError):
            validate_state([-1], [[2]], [[1]])

    def test_wrong_vector_length(self):
        with self.assertRaises(ValueError):
            validate_state([1, 1], [[2]], [[1]])

    def test_bad_process_number(self):
        with self.assertRaises(ValueError):
            deadlock.request_resources(pid=9, request=[0, 0, 0], **SAMPLE)

    def test_non_numeric_vector(self):
        with self.assertRaises(ValueError):
            parse_vector("1 a 2", 3)


if __name__ == "__main__":
    unittest.main()
