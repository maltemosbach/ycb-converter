"""Convert URDF models to USD."""

from . import DATA_DIR, YCB_OBJECT_NAMES
import os
from os import PathLike
import pathlib
from tqdm import tqdm


def convert_urdf_to_usd(object_name: str, orbit_path: str | PathLike, show: bool = False) -> None:
    orbit_path = pathlib.Path(orbit_path)
    urdf_path = DATA_DIR / "urdfs" / (object_name + ".urdf")

    if not urdf_path.exists():
        return

    usd_path = DATA_DIR / "usds" / object_name / (object_name + ".usd")
    if not usd_path.exists():
        usd_path.parent.mkdir(parents=True, exist_ok=True)

    command = f"python {orbit_path / 'source/standalone/tools/convert_urdf.py'} {urdf_path} {usd_path} --make-instanceable"

    if not show:
        command += " --headless"

    os.system(command)


def convert_urdfs_to_usds(orbit_path: str | PathLike) -> None:
    for object_name in tqdm(YCB_OBJECT_NAMES, desc="Converting URDFs to USDs"):
        convert_urdf_to_usd(object_name, orbit_path)

