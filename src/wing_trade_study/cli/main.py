"""Command line interface for environment diagnostics and study orchestration."""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import json
import sys
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class PackageStatus:
    """Import result for a required package."""

    package: str
    available: bool
    version: str | None
    error: str | None


def _check_package(package: str) -> PackageStatus:
    try:
        module = importlib.import_module(package)
    except Exception as exc:  # pragma: no cover - exercised in integration smoke
        return PackageStatus(
            package=package, available=False, version=None, error=str(exc)
        )

    try:
        version = importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        module_file = getattr(module, "__file__", "<unknown>")
        return PackageStatus(
            package=package,
            available=False,
            version=None,
            error=(
                f"{package} distribution not installed "
                f"(resolved module: {module_file})"
            ),
        )

    return PackageStatus(package=package, available=True, version=version, error=None)


def run_doctor() -> int:
    """Run a solver-stack import check and print machine-readable output."""
    required = ("openmdao", "mphys", "tacs")
    statuses = [_check_package(package) for package in required]
    payload = {
        "required_packages": [asdict(status) for status in statuses],
        "all_available": all(status.available for status in statuses),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["all_available"] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wing_trade_study", description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("doctor", help="check OpenMDAO/MPhys/TACS availability")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "doctor":
        return run_doctor()

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
