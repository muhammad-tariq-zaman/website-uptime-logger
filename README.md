# website-uptime-logger

Check URLs with `urllib` and append timestamp, status, and latency to a CSV log.

## How to run

```bash
python3 main.py https://example.com https://example.org --csv uptime.csv
```

## Example output (sample from test fixture data)

```text
https://example.test  200  12.3 ms
Logged to uptime.csv
```

Tests mock `urllib`, so they run without network access.
