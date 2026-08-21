"""Offline tests for the NERDD module-discovery helpers."""

from __future__ import annotations

import importlib.util
import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


SCRIPTS = Path(__file__).parents[1] / "nerdd-molecular-predictions" / "scripts"

LIST_MODULES_SCRIPT = SCRIPTS / "list_modules.py"
SPEC = importlib.util.spec_from_file_location("nerdd_list_modules", LIST_MODULES_SCRIPT)
assert SPEC and SPEC.loader
list_modules = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(list_modules)

GET_MODULE_SCRIPT = SCRIPTS / "get_module.py"
SPEC = importlib.util.spec_from_file_location("nerdd_get_module", GET_MODULE_SCRIPT)
assert SPEC and SPEC.loader
get_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(get_module)


class ModuleDiscoveryTests(unittest.TestCase):
    def test_list_modules(self) -> None:
        modules = [
            {"id": "glory", "name": "GLORY", "version": "3.0"},
            {"id": "cypstrate", "name": "CYPstrate", "version": "1.0"},
        ]
        stdout = io.StringIO()

        with (
            patch.object(list_modules, "get_json", return_value=modules) as get_json,
            patch("sys.argv", [str(LIST_MODULES_SCRIPT), "--api-url", "https://example.test/api/"]),
            redirect_stdout(stdout),
        ):
            self.assertEqual(list_modules.main(), 0)

        get_json.assert_called_once_with("https://example.test/api/modules")
        self.assertEqual(json.loads(stdout.getvalue()), modules)

    def test_get_module(self) -> None:
        module = {
            "id": "cypstrate",
            "name": "CYPstrate",
            "job_parameters": [{"name": "prediction_mode"}],
        }
        stdout = io.StringIO()

        with (
            patch.object(get_module, "get_json", return_value=module) as get_json,
            patch(
                "sys.argv",
                [str(GET_MODULE_SCRIPT), "cypstrate", "--api-url", "https://example.test/api/"],
            ),
            redirect_stdout(stdout),
        ):
            self.assertEqual(get_module.main(), 0)

        get_json.assert_called_once_with("https://example.test/api/modules/cypstrate")
        self.assertEqual(json.loads(stdout.getvalue()), module)
