from os import PathLike
from typing import Optional
from ycb_converter.download_ycb_models import download_ycb_models
from ycb_converter.align_to_origin import align_meshes_to_origin
from ycb_converter.convex_decompose import convex_decompose_meshes
from ycb_converter.assemble_urdf import assemble_meshes_to_urdfs
from ycb_converter.convert_to_usd import convert_urdfs_to_usds


def main(orbit_path: Optional[str | PathLike] = None, resolution: str = "16k", threshold: float = 0.05, face_count: int = 100) -> None:
    download_ycb_models(resolution=resolution)
    align_meshes_to_origin(resolution=resolution)
    convex_decompose_meshes(resolution=resolution, threshold=threshold, face_count=face_count)
    assemble_meshes_to_urdfs(resolution=resolution)

    if orbit_path is not None:
        convert_urdfs_to_usds(orbit_path=orbit_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert YCB models to sim-ready assets.")
    parser.add_argument("--orbit-path", type=str, default=None, help="Path to the Orbit binary.")
    parser.add_argument("--resolution", type=str, default="16k", help="Resolution of meshes to align.")
    parser.add_argument("--threshold", type=float, default=0.05, help="Threshold for convex decomposition.")
    parser.add_argument("--face-count", type=int, default=100, help="Face count for convex decomposition.")
    args = parser.parse_args()
    main(orbit_path=args.orbit_path, resolution=args.resolution, threshold=args.threshold, face_count=args.face_count)
