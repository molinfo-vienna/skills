#!/usr/bin/env python3
"""Create a NERDD prediction job from new molecular input."""

from __future__ import annotations

import argparse
import json
import mimetypes
import sys
import uuid
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_API = "https://nerdd.univie.ac.at/api"


def read_json(request: Request) -> Any:
    with urlopen(request, timeout=60) as response:
        return json.load(response)


def add_part(
    parts: list[bytes],
    boundary: str,
    name: str,
    value: str | bytes,
    *,
    filename: str | None = None,
    content_type: str | None = None,
) -> None:
    disposition = f'Content-Disposition: form-data; name="{name}"'
    if filename is not None:
        disposition += f'; filename="{filename}"'
    headers = [f"--{boundary}", disposition]
    if content_type:
        headers.append(f"Content-Type: {content_type}")
    parts.append(("\r\n".join(headers) + "\r\n\r\n").encode())
    parts.append(value.encode() if isinstance(value, str) else value)
    parts.append(b"\r\n")


def multipart_body(
    inputs: list[str], params: dict[str, Any], files: list[Path]
) -> tuple[str, bytes]:
    boundary = f"----nerdd-{uuid.uuid4().hex}"
    parts: list[bytes] = []
    for input_text in inputs:
        add_part(parts, boundary, "inputs", input_text)
    for name, value in params.items():
        # FastAPI form fields accept scalar strings; JSON preserves bools and numbers.
        add_part(
            parts,
            boundary,
            name,
            json.dumps(value) if not isinstance(value, str) else value,
        )
    for path in files:
        add_part(
            parts,
            boundary,
            "files",
            path.read_bytes(),
            filename=path.name,
            content_type=mimetypes.guess_type(path.name)[0]
            or "application/octet-stream",
        )
    parts.append(f"--{boundary}--\r\n".encode())
    return boundary, b"".join(parts)


def parse_param(item: str) -> tuple[str, Any]:
    if "=" not in item or item.startswith("="):
        raise ValueError("parameters must use NAME=VALUE")
    name, raw_value = item.split("=", 1)
    try:
        return name, json.loads(raw_value)
    except json.JSONDecodeError:
        return name, raw_value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--module", required=True, help="NERDD module ID, e.g. cypstrate"
    )
    parser.add_argument(
        "--input", action="append", default=[], help="Molecular input (repeatable)"
    )
    parser.add_argument(
        "--file", action="append", default=[], help="Input file to upload (repeatable)"
    )
    parser.add_argument(
        "--param",
        action="append",
        default=[],
        help="Module parameter as NAME=VALUE (repeatable)",
    )
    parser.add_argument("--api-url", default=DEFAULT_API, help="NERDD API base URL")
    args = parser.parse_args()

    inputs = list(args.input)
    paths = [Path(item) for item in args.file]
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        parser.error("input file(s) not found: " + ", ".join(missing))
    if not (inputs or paths):
        parser.error("provide at least one --input or --file")
    try:
        params = dict(parse_param(item) for item in args.param)
        boundary, body = multipart_body(inputs, params, paths)
        api_url = args.api_url.rstrip("/")
        create = Request(
            f"{api_url}/{args.module}/jobs",
            data=body,
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
        )
        print(json.dumps(read_json(create), ensure_ascii=False))
        return 0
    except (
        HTTPError,
        URLError,
        TimeoutError,
        OSError,
        ValueError,
        json.JSONDecodeError,
    ) as error:
        detail = (
            error.read().decode(errors="replace")
            if isinstance(error, HTTPError)
            else str(error)
        )
        print(f"NERDD API request failed: {detail}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
