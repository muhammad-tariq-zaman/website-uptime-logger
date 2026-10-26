"""Website uptime logger: check URLs and log timestamp/status/latency to CSV."""
import argparse
import csv
import datetime
import os
import sys
import time
import urllib.error
import urllib.request


def check_url(url, timeout=10):
    start = time.monotonic()
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            status = resp.status
            resp.read(1)
    except urllib.error.HTTPError as exc:
        status = exc.code
    except Exception as exc:
        return {"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "url": url, "status": "ERROR", "latency_ms": round((time.monotonic() - start) * 1000, 1),
                "error": str(exc)}
    latency = round((time.monotonic() - start) * 1000, 1)
    return {"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "url": url, "status": status, "latency_ms": latency, "error": ""}


def log_results(results, csv_path):
    new = not os.path.exists(csv_path)
    with open(csv_path, "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["timestamp", "url", "status", "latency_ms", "error"])
        if new:
            w.writeheader()
        w.writerows(results)
    return csv_path


def main(argv=None):
    p = argparse.ArgumentParser(description="Log website uptime checks to CSV.")
    p.add_argument("urls", nargs="+")
    p.add_argument("--csv", default="uptime.csv")
    p.add_argument("--timeout", type=int, default=10)
    args = p.parse_args(argv)
    results = [check_url(u, args.timeout) for u in args.urls]
    for r in results:
        print(f"{r['url']}  {r['status']}  {r['latency_ms']} ms")
    log_results(results, args.csv)
    print(f"Logged to {args.csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
