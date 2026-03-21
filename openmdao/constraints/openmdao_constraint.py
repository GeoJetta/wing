"""OpenMDAO constraint definitions for wing trade study.

This module provides a reusable helper for adding common constraint
expressions to an OpenMDAO model. It is intentionally minimal so the
project can extend it with discipline-specific constraints.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class ConstraintSpec:
    """Container describing a single OpenMDAO constraint."""

    name: str
    lower: float | None = None
    upper: float | None = None
    equals: float | None = None
    ref: float | None = None


def add_constraints(model, constraints: Iterable[ConstraintSpec]) -> None:
    """Add a collection of constraints to an OpenMDAO model.

    Parameters
    ----------
    model:
        OpenMDAO System/Group/Problem-like object that implements
        ``add_constraint``.
    constraints:
        Iterable of :class:`ConstraintSpec` entries.
    """

    for spec in constraints:
        kwargs = {
            "lower": spec.lower,
            "upper": spec.upper,
            "equals": spec.equals,
            "ref": spec.ref,
        }
        filtered_kwargs = {k: v for k, v in kwargs.items() if v is not None}
        model.add_constraint(spec.name, **filtered_kwargs)


DEFAULT_CONSTRAINTS: tuple[ConstraintSpec, ...] = (
    ConstraintSpec(name="stress_margin", lower=0.0),
    ConstraintSpec(name="buckling_margin", lower=0.0),
    ConstraintSpec(name="tip_deflection", upper=1.0),
)
