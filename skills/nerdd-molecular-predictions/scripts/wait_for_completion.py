#!/usr/bin/env python3
"""Wait for a NERDD job to reach a terminal state."""

from __future__ import annotations

import argparse
import json
import sys
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_API = "https://nerdd.univie.ac.at/api"
TERMINAL_STATUSES = {"completed", "failed"}
POLL_INTERVAL_SECONDS = 5
TIMEOUT_SECONDS = 3600


def get_json(url: str) -> Any:
    request = Request(url, headers={"Accept": "application/json"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job_id", help="NERDD job ID")
    parser.add_argument("--api-url", default=DEFAULT_API, help="NERDD API base URL")
    args = parser.parse_args()
    api_url = args.api_url.rstrip("/")

    try:
        deadline = time.monotonic() + TIMEOUT_SECONDS
        while True:
            job = get_json(f"{api_url}/jobs/{args.job_id}")
            if job.get("status") in TERMINAL_STATUSES:
                print(json.dumps(job, ensure_ascii=False))
                if job["status"] == "failed":
                    print(f"NERDD job failed: {job.get('id')}", file=sys.stderr)
                    return 1
                return 0
            if time.monotonic() >= deadline:
                print(json.dumps(job, ensure_ascii=False), file=sys.stderr)
                print(
                    f"Timed out after {TIMEOUT_SECONDS} seconds; job ID: {job.get('id')}",
                    file=sys.stderr,
                )
                return 2
            time.sleep(POLL_INTERVAL_SECONDS)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        detail = error.read().decode(errors="replace") if isinstance(error, HTTPError) else str(error)
        print(f"NERDD API request failed: {detail}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
