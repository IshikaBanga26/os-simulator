import unittest
from modules import scheduler
from utils.validation import validate_processes, validate_quantum

BASIC = [
    {"pid": "P1", "arrival": 0, "burst": 5, "priority": 2},
    {"pid": "P2", "arrival": 1, "burst": 3, "priority": 1},
    {"pid": "P3", "arrival": 2, "burst": 2, "priority": 3},
]


def by_pid(results):
    return {r["pid"]: r for r in results}


class TestValidScheduling(unittest.TestCase):
    def test_fcfs_waiting_time(self):
        self.assertEqual(by_pid(scheduler.fcfs(BASIC))["P2"]["waiting"], 4)

    def test_sjf_runs_shortest_ready_job_first(self):
        r = by_pid(scheduler.sjf(BASIC))
        # At time 5, P2 (burst 3) and P3 (burst 2) are waiting: P3 is shorter, so it runs first.
        self.assertEqual(r["P3"]["finish"], 7)
        self.assertEqual(r["P2"]["finish"], 10)

    def test_round_robin_finish_times(self):
        r = by_pid(scheduler.round_robin(BASIC, 2))
        self.assertEqual(r["P3"]["finish"], 6)
        self.assertEqual(r["P1"]["finish"], 10)

    def test_averages(self):
        a = scheduler.averages(scheduler.fcfs(BASIC))
        self.assertIn("avg_waiting", a)


class TestBoundary(unittest.TestCase):
    def test_single_process(self):
        r = scheduler.fcfs([{"pid": "P1", "arrival": 0, "burst": 1}])
        self.assertEqual(r[0]["waiting"], 0)

    def test_cpu_idle_gap(self):
        r = scheduler.fcfs([{"pid": "P1", "arrival": 5, "burst": 2}])
        self.assertEqual(r[0]["start"], 5)
        self.assertEqual(r[0]["waiting"], 0)

    def test_quantum_larger_than_burst(self):
        r = scheduler.round_robin([{"pid": "P1", "arrival": 0, "burst": 3}], 10)
        self.assertEqual(r[0]["finish"], 3)


class TestInvalidInput(unittest.TestCase):
    def test_empty_list(self):
        with self.assertRaises(ValueError):
            validate_processes([])

    def test_negative_burst(self):
        with self.assertRaises(ValueError):
            validate_processes([{"pid": "P1", "arrival": 0, "burst": -5}])

    def test_zero_burst(self):
        with self.assertRaises(ValueError):
            validate_processes([{"pid": "P1", "arrival": 0, "burst": 0}])

    def test_negative_arrival(self):
        with self.assertRaises(ValueError):
            validate_processes([{"pid": "P1", "arrival": -1, "burst": 2}])

    def test_duplicate_pid(self):
        p = {"pid": "P1", "arrival": 0, "burst": 2}
        with self.assertRaises(ValueError):
            validate_processes([p, dict(p)])

    def test_zero_quantum(self):
        with self.assertRaises(ValueError):
            validate_quantum(0)


if __name__ == "__main__":
    unittest.main()
