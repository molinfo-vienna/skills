#!/usr/bin/env python3
"""Print the live NERDD module list as JSON."""

from __future__ import annotations

import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_API = "https://nerdd.univie.ac.at/api"


def get_json(url: str) -> object:
    request = Request(url, headers={"Accept": "application/json"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api-url", default=DEFAULT_API, help="NERDD API base URL")
    args = parser.parse_args()
    api_url = args.api_url.rstrip("/")

    try:
        modules = get_json(f"{api_url}/modules")
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        print(f"NERDD API request failed: {error}", file=sys.stderr)
        return 1

    print(json.dumps(modules, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
