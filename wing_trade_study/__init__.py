"""Development-time package shim to support ``python -m wing_trade_study...``."""

from __future__ import annotations

from pathlib import Path

__all__ = ["__version__"]
__version__ = "0.1.0"

_src_package = Path(__file__).resolve().parent.parent / "src" / "wing_trade_study"
if _src_package.is_dir():
    __path__.append(str(_src_package))
