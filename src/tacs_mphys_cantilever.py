"""Cantilever strut setup using MPhys/TacsBuilder (no direct pyTACS component).

This script:
1) builds a parametric BDF for the cantilever + optional strut,
2) wires a structural scenario using MPhys + TacsBuilder,
3) runs a single analysis point,
4) writes a simple 3D geometry preview image from the generated TACS input geometry.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import openmdao.api as om
from mphys import Multipoint
from mphys.scenarios import ScenarioStructural
from mphys.tacs import TacsBuilder

from constraints import WingStrutDesign, validate_design

RHO = 2780.0
E = 73.1e9
NU = 0.33
YIELD = 324.0e6


class CantileverStructModel(Multipoint):
    def initialize(self):
        self.options.declare("bdf_path", types=str)

    def setup(self):
        struct_builder = TacsBuilder(
            mesh_file=self.options["bdf_path"],
            element_callback=self._element_callback,
            problem_setup=self._problem_setup,
        )
        struct_builder.initialize(self.comm)
        self.add_subsystem("mesh", struct_builder.get_mesh_coordinate_subsystem())

        self.mphys_add_scenario(
            "cruise",
            ScenarioStructural(struct_builder=struct_builder),
            coupling_nonlinear_solver=om.NonlinearBlockGS(maxiter=20),
            coupling_linear_solver=om.LinearBlockGS(maxiter=20),
        )

    @staticmethod
    def _element_callback(dv_num, comp_id, comp_descript, elem_descripts, special_dvs, **kwargs):
        # TACS material/constitutive setup can be customized here per component.
        # Keeping callback present (and explicit) for later DV mapping.
        return None

    @staticmethod
    def _problem_setup(scenario_name, problem):
        problem.addFunction("mass", "StructuralMass")
        problem.addFunction("ks_vmfailure", "KSFailure", ksWeight=50.0)


def _box_section(width: float, depth: float, t: float):
    wi = max(width - 2.0 * t, 1e-4)
    di = max(depth - 2.0 * t, 1e-4)
    area = width * depth - wi * di
    iy = (width * depth**3 - wi * di**3) / 12.0
    iz = (depth * width**3 - di * wi**3) / 12.0
    j = iy + iz
    return area, iy, iz, j


def build_bdf(design: WingStrutDesign, path: Path, nspan: int = 16) -> np.ndarray:
    validate_design(design)
    span_stations = np.linspace(0.0, design.span, nspan)

    widths = np.interp(
        span_stations,
        [0.0, 0.5 * design.span, design.span],
        [design.root_box_width * design.r_1, design.root_box_width * design.r_2, design.tip_box_width * design.r_3],
    )
    depths = design.depth_ratio * widths

    with path.open("w", encoding="utf-8") as f:
        f.write("SOL 101\nCEND\nBEGIN BULK\n")
        f.write("MAT1,1,{:.6e},,{:.6f},{:.6e}\n".format(E, NU, RHO))

        nid = 1
        beam_nodes = []
        for y in span_stations:
            beam_nodes.append((nid, 0.0, y, 0.0))
            f.write(f"GRID,{nid},,0.0,{y:.6f},0.0\n")
            nid += 1

        pid = 1
        eid = 1
        for i in range(nspan - 1):
            a, iy, iz, j = _box_section(widths[i], depths[i], design.t_wb)
            f.write(f"PBAR,{pid},1,{a:.6e},{iy:.6e},{iz:.6e},{j:.6e}\n")
            n1 = i + 1
            n2 = i + 2
            f.write(f"CBAR,{eid},{pid},{n1},{n2},0.0,0.0,1.0\n")
            pid += 1
            eid += 1

        # root clamp
        f.write("SPC1,1,123456,1\n")

        # optional strut branch (pin to span node and aft/lower ground anchor)
        geometry_pts = np.array([[x, y, z] for _, x, y, z in beam_nodes], dtype=float)
        if design.use_strut:
            sid = int(np.argmin(np.abs(span_stations - design.eta_s * design.span))) + 1
            root_anchor = nid
            tip_anchor = nid + 1
            x_strut = 0.0
            y_strut = span_stations[sid - 1]
            z_strut = 0.0
            geometry_pts = np.vstack((geometry_pts, [x_strut, y_strut, z_strut]))
            geometry_pts = np.vstack((geometry_pts, [design.x_aft, y_strut + 0.5, -2.0]))

            f.write(f"GRID,{root_anchor},,{x_strut:.6f},{y_strut:.6f},{z_strut:.6f}\n")
            f.write(f"GRID,{tip_anchor},,{design.x_aft:.6f},{y_strut + 0.5:.6f},-2.0\n")

            a, iy, iz, j = _box_section(design.w_strut, 0.75 * design.w_strut, design.t_strut)
            f.write(f"PBAR,{pid},1,{a:.6e},{iy:.6e},{iz:.6e},{j:.6e}\n")
            f.write(f"CBAR,{eid},{pid},{root_anchor},{tip_anchor},0.0,1.0,0.0\n")

            # RBE2 ties strut root to selected span station
            f.write(f"RBE2,{eid+1},{sid},123456,{root_anchor}\n")

            # pin the lower anchor translationally
            f.write(f"SPC1,2,123,{tip_anchor}\n")

        # tip load
        f.write(f"FORCE,10,{nspan},,1.0,0.0,0.0,-1.0e5\n")
        f.write("LOAD,3,1.0,10\n")
        f.write("ENDDATA\n")

    return geometry_pts


def save_geometry_plot(points: np.ndarray, path: Path) -> None:
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(points[:, 0], points[:, 1], points[:, 2], "o-", lw=2)
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_zlabel("z [m]")
    ax.set_title("Cantilever + Strut Geometry Passed to TACS")
    ax.view_init(elev=22, azim=-60)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def main(out_dir: str = "outputs"):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    design = WingStrutDesign()
    bdf_path = out / "cantilever_strut.bdf"
    points = build_bdf(design, bdf_path)

    prob = om.Problem()
    prob.model = CantileverStructModel(bdf_path=str(bdf_path))
    prob.setup()
    prob.run_model()

    save_geometry_plot(points, out / "tacs_geometry.png")
    print(f"Wrote BDF: {bdf_path}")
    print(f"Wrote geometry image: {out / 'tacs_geometry.png'}")


if __name__ == "__main__":
    main()
