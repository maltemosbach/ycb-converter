from os import PathLike
from typing import Optional
from ycb_converter.download_ycb_models import download_ycb_models
from ycb_converter.align_to_origin import align_meshes_to_origin
from ycb_converter.convex_decompose import convex_decompose_meshes
from ycb_converter.assemble_urdf import assemble_meshes_to_urdfs
from ycb_converter.convert_to_usd import convert_urdfs_to_usds


def main(orbit_path: Optional[str | PathLike] = None, resolution: str = "16k", threshold: float = 0.07, max_convex_hull: int = -1, face_density: int = 7500) -> None:
    download_ycb_models(resolution=resolution)
    align_meshes_to_origin(resolution=resolution)
    convex_decompose_meshes(resolution=resolution, threshold=threshold, max_convex_hull=max_convex_hull, face_density=face_density)
    assemble_meshes_to_urdfs(resolution=resolution)

    if orbit_path is not None:
        convert_urdfs_to_usds(orbit_path=orbit_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert YCB models to sim-ready assets.")
    parser.add_argument("--orbit-path", type=str, default=None, help="Path to the Orbit binary.")
    parser.add_argument("--resolution", type=str, default="16k", help="Resolution of meshes to align.")
    parser.add_argument("--threshold", type=float, default=0.07, help="Threshold for convex decomposition.")
    parser.add_argument("--max-convex-hull", type=int, default=16, help="Maximum number of convex hulls in the resulting decomposition.")
    parser.add_argument("--face-density", type=int, default=7500, help="Target face count / area for each convex collision mesh.")

    args = parser.parse_args()
    main(orbit_path=args.orbit_path, resolution=args.resolution, threshold=args.threshold, max_convex_hull=args.max_convex_hull, face_density=args.face_density)
