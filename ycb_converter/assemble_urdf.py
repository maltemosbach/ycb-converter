"""Assemble URDFs from meshes and inertial properties."""

from . import DATA_DIR, get_mesh_directory, YCB_OBJECT_NAMES
import glob
import json
from os import PathLike
import pathlib
from tqdm import tqdm
import trimesh
from typing import Any, Dict, List
from yourdfpy import URDF


def urdf_template(object_name: str, visual_mesh_path: str | PathLike, collision_mesh_paths: List[str | PathLike],
                  inertial_properties: Dict[str, Any]) -> str:
    urdf_str = f"""<?xml version="1.0"?>
    <robot name="{object_name}">
        <link name="base_link">
            <inertial>
                <origin xyz="{inertial_properties['center_of_mass'][0]} {inertial_properties['center_of_mass'][1]} {inertial_properties['center_of_mass'][2]}"/>
                <mass value="{inertial_properties['mass']}"/>
                <inertia ixx="{inertial_properties['moment_inertia']['ixx']}" ixy="{inertial_properties['moment_inertia']['ixy']}" ixz="{inertial_properties['moment_inertia']['ixz']}" iyy="{inertial_properties['moment_inertia']['iyy']}" iyz="{inertial_properties['moment_inertia']['iyz']}" izz="{inertial_properties['moment_inertia']['izz']}"/>
            </inertial>
            <visual>
                <geometry>
                    <mesh filename="{visual_mesh_path}"/>
                </geometry>
            </visual>"""

    for collision_mesh_path in collision_mesh_paths:
        urdf_str += f"""
            <collision>
                <geometry>
                    <mesh filename="{collision_mesh_path}"/>
                </geometry>
            </collision>"""

    urdf_str += """
        </link>
    </robot>
    """
    return urdf_str


def assemble_mesh_to_urdf(object_name: str, resolution: str = "16k") -> trimesh.Scene:
    visual_mesh_path = ".." / (get_mesh_directory(object_name, resolution) / "centered.obj").relative_to(DATA_DIR)
    collision_mesh_paths = [".." / pathlib.Path(collider).relative_to(DATA_DIR) for collider in sorted(
        glob.glob(str(get_mesh_directory(object_name, resolution) / "convex_collider_*.obj")))]

    with open(get_mesh_directory(object_name) / "inertial_properties.json", 'r') as f:
        inertial_properties = json.load(f)

    urdf_str = urdf_template(object_name, visual_mesh_path, collision_mesh_paths, inertial_properties)

    if not (DATA_DIR / "urdfs").exists():
        (DATA_DIR / "urdfs").mkdir(parents=True, exist_ok=True)

    with open(DATA_DIR / "urdfs" / (object_name + ".urdf"), "w") as urdf_file:
        urdf_file.write(urdf_str)

    return URDF.load(DATA_DIR / "urdfs" / (object_name + ".urdf"), mesh_dir=DATA_DIR / "urdfs")._scene


def assemble_meshes_to_urdfs(resolution: str = "16k") -> None:
    for object_name in tqdm(YCB_OBJECT_NAMES, desc="Converting meshes to URDFs"):
        if pathlib.Path.exists(get_mesh_directory(object_name, resolution) / "centered.obj"):
            assemble_mesh_to_urdf(object_name, resolution=resolution)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Decompose meshes into convex colliders and infer inertial properties.")
    parser.add_argument("--resolution", type=str, default="16k", help="Resolution of meshes to use in URDFs.")
    args = parser.parse_args()
    assemble_meshes_to_urdfs(resolution=args.resolution)
