"""Constraint and geometry definitions for the cantilever + optional strut model.

This module encodes the variables referenced in the design guidance:
r_1, r_2, r_3, t_wb, eta_s, x_aft, w_strut, t_strut.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WingStrutDesign:
    span: float = 15.0
    root_box_width: float = 1.8
    tip_box_width: float = 0.45
    depth_ratio: float = 0.14

    # Wing box width controls at 3 span stations
    r_1: float = 1.0
    r_2: float = 0.85
    r_3: float = 0.70

    # Wing box wall thickness
    t_wb: float = 0.015

    # Strut position and geometry
    eta_s: float = 0.55
    x_aft: float = 2.0
    w_strut: float = 0.20
    t_strut: float = 0.010

    use_strut: bool = True


BOUNDS = {
    "r_1": (0.4, 1.4),
    "r_2": (0.4, 1.4),
    "r_3": (0.4, 1.4),
    "t_wb": (0.003, 0.050),
    "eta_s": (0.20, 0.90),
    "x_aft": (0.50, 5.00),
    "w_strut": (0.05, 0.50),
    "t_strut": (0.003, 0.050),
}


def validate_design(design: WingStrutDesign) -> None:
    """Raise ValueError if a design variable is out-of-bounds."""
    for var, (lb, ub) in BOUNDS.items():
        val = getattr(design, var)
        if val < lb or val > ub:
            raise ValueError(f"{var}={val} outside [{lb}, {ub}]")
