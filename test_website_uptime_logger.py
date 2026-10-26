import csv
import io
import os
import sys
import tempfile
import unittest
import urllib.error
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import main


class FakeResp:
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def read(self, n=-1):
        return b"x"


class TestUptime(unittest.TestCase):
    def test_ok_and_error(self):
        with mock.patch("main.urllib.request.urlopen", return_value=FakeResp()):
            r = main.check_url("https://example.test")
        self.assertEqual(r["status"], 200)
        with mock.patch("main.urllib.request.urlopen",
                        side_effect=urllib.error.URLError("no route")):
            r = main.check_url("https://bad.test")
        self.assertEqual(r["status"], "ERROR")

    def test_csv_log(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "up.csv")
            main.log_results([{"timestamp": "2026-10-26T00:00:00+00:00",
                               "url": "https://example.test", "status": 200,
                               "latency_ms": 12.3, "error": ""}], path)
            rows = list(csv.DictReader(open(path)))
            self.assertEqual(rows[0]["url"], "https://example.test")
            self.assertEqual(rows[0]["status"], "200")


if __name__ == "__main__":
    unittest.main()
