"""Smoke tests for M0 environment bring-up."""

from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
from importlib import metadata


def _can_import(package: str) -> bool:
    try:
        importlib.import_module(package)
    except Exception:
        return False
    return True


def _has_distribution(package: str) -> bool:
    try:
        metadata.version(package)
    except metadata.PackageNotFoundError:
        return False
    return True


def test_import_and_distribution_status_are_consistent() -> None:
    required_packages = ("openmdao", "mphys", "tacs")

    for package in required_packages:
        imported = _can_import(package)
        has_distribution = _has_distribution(package)
        assert imported == has_distribution


def test_doctor_command_reports_json_status_and_exit_code() -> None:
    env = dict(os.environ)
    env["PYTHONPATH"] = "src"

    result = subprocess.run(
        [sys.executable, "-m", "wing_trade_study.cli.main", "doctor"],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    payload = json.loads(result.stdout)
    assert set(payload.keys()) == {"all_available", "required_packages"}
    assert len(payload["required_packages"]) == 3

    available_flags = [entry["available"] for entry in payload["required_packages"]]
    assert payload["all_available"] == all(available_flags)
    expected_return_code = 0 if payload["all_available"] else 1
    assert result.returncode == expected_return_code
