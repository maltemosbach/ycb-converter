"""Align meshes to a canonical origin."""

from . import get_mesh_directory, YCB_OBJECT_NAMES
import pathlib
from tqdm import tqdm
import trimesh


def to_origin(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    transform, extents = trimesh.bounds.oriented_bounds(mesh)
    mesh.apply_transform(transform)
    return mesh


def align_mesh_to_origin(object_name: str, resolution: str = "16k") -> None:
    mesh = trimesh.load(get_mesh_directory(object_name, resolution) / "textured.obj")
    mesh = to_origin(mesh)
    mesh.export(get_mesh_directory(object_name, resolution) / "centered.obj")


def align_meshes_to_origin(resolution: str = "16k") -> None:
    for object_name in tqdm(YCB_OBJECT_NAMES, desc="Converting meshes to origin"):
        if pathlib.Path.exists(get_mesh_directory(object_name, resolution) / "textured.obj"):
            align_mesh_to_origin(object_name, resolution=resolution)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Align meshes to a canonical origin.")
    parser.add_argument("--resolution", type=str, default="16k", help="Resolution of meshes to align.")
    args = parser.parse_args()
    align_meshes_to_origin(resolution=args.resolution)
