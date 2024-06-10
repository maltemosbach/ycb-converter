"""Decompose meshes into convex colliders and infer inertial properties."""

from . import DATA_DIR, get_mesh_directory, YCB_OBJECT_NAMES
import coacd
import json
import pathlib
from tqdm import tqdm
import trimesh
from typing import List, Optional


def to_convex_colliders(mesh: trimesh.Trimesh, threshold: float = 0.07, max_convex_hull: int = -1, face_density: Optional[int] = None, 
        min_faces: int = 12, max_faces: int = 100, preprocess_resolution: int = 10) -> List[trimesh.Trimesh]:
    coacd_mesh = coacd.Mesh(mesh.vertices, mesh.faces)
    convex_meshes = [trimesh.Trimesh(vs, fs) for vs, fs in coacd.run_coacd(coacd_mesh, threshold=threshold, max_convex_hull=max_convex_hull, preprocess_resolution=preprocess_resolution)]
    if face_density is not None:
        return [convex_mesh.simplify_quadric_decimation(max(min(int(face_density * convex_mesh.area), max_faces), min_faces)) for convex_mesh in convex_meshes]
    return convex_meshes


def infer_inertial_properties(object_name: str, convex_colliders: List[trimesh.Trimesh], resolution: str = "16k") -> None:
    with open(DATA_DIR / "weights.json", 'r') as f:
        weights = json.load(f)

    if weights[object_name] is None:
        raise ValueError(f"Weight of object '{object_name}' is not available.")

    object_volume = sum([c.volume for c in convex_colliders])
    for c in convex_colliders:
        c.density = weights[object_name] / object_volume

    scene = trimesh.Scene(convex_colliders)

    inertial_properties = {
        "mass": weights[object_name],
        "center_of_mass": scene.center_mass.tolist(),
        "moment_inertia": {
            "ixx": scene.moment_inertia[0, 0],
            "ixy": scene.moment_inertia[0, 1],
            "ixz": scene.moment_inertia[0, 2],
            "iyy": scene.moment_inertia[1, 1],
            "iyz": scene.moment_inertia[1, 2],
            "izz": scene.moment_inertia[2, 2]
        }
    }

    with open(get_mesh_directory(object_name, resolution) / "inertial_properties.json", 'w') as f:
        json.dump(inertial_properties, f, indent=4)


def convex_decompose_mesh(object_name: str, resolution: str = "16k", threshold: float = 0.07, max_convex_hull: int = -1, face_density: Optional[int] = None) -> None:
    # Infer convex decomposition from mesh.
    mesh = trimesh.load(get_mesh_directory(object_name, resolution) / "centered.obj")
    convex_meshes = to_convex_colliders(mesh, threshold=threshold, max_convex_hull=max_convex_hull, face_density=face_density)

    # Infer and save inertial properties of decomposed mesh.
    infer_inertial_properties(object_name, convex_meshes, resolution)

    for i, convex_mesh in enumerate(convex_meshes):
        convex_mesh.export(get_mesh_directory(object_name, resolution) / f"convex_collider_{i}.obj")


def convex_decompose_meshes(resolution: str = "16k", threshold: float = 0.07, max_convex_hull: int = -1, face_density: Optional[int] = None) -> None:
    for object_name in tqdm(YCB_OBJECT_NAMES, desc="Converting meshes to convex colliders"):
        if pathlib.Path.exists(get_mesh_directory(object_name, resolution) / "centered.obj"):
            convex_decompose_mesh(object_name, resolution=resolution, threshold=threshold, max_convex_hull=max_convex_hull, face_density=face_density)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Decompose meshes into convex colliders and infer inertial properties.")
    parser.add_argument("--resolution", type=str, default="16k", help="Resolution of meshes to decompose.")
    parser.add_argument("--threshold", type=float, default=0.07, help="Threshold for convex decomposition.")
    parser.add_argument("--max-convex-hull", type=int, default=16, help="Maximum number of convex hulls in the resulting decomposition.")
    parser.add_argument("--face-density", type=int, default=7500, help="Target face count / area for each convex collision mesh.")
    args = parser.parse_args()
    convex_decompose_meshes(resolution=args.resolution, threshold=args.threshold, max_convex_hull=args.max_convex_hull, face_density=args.face_density)
