import json
from pathlib import Path
from urllib.request import urlopen

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
YCB_DATA_URL = "http://ycb-benchmarks.s3-website-us-east-1.amazonaws.com/data/"
YCB_OBJECT_NAMES = json.loads(urlopen(YCB_DATA_URL + "objects.json").read())["objects"]


def get_mesh_directory(object_name: str, resolution: str = "16k") -> Path:
    if resolution not in ["16k", "64k", "512k"]:
        raise ValueError("Invalid resolution. Choose from '16k', '64k', or '512k'.")
    return DATA_DIR / "meshes" / object_name / f"google_{resolution}"
