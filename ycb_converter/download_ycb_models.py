"""Download the original YCB models."""

from . import DATA_DIR, YCB_DATA_URL, YCB_OBJECT_NAMES
import os
from tqdm import tqdm
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def download_file(url: str, filename: str) -> None:
    u = urlopen(url)

    with open(filename, 'wb') as f:
        f.write(u.read())


def extract_tar_archive(filename: str, dir: str) -> None:
    os.system(f"tar -xzf {filename} -C {dir}")
    os.remove(filename)


def url_exists(url: str) -> bool:
    try:
        request = Request(url)
        _ = urlopen(request)
        return True
    except HTTPError:
        return False


def download_ycb_models(resolution: str = "16k") -> None:
    download_dir = DATA_DIR / "meshes"
    if resolution not in ["16k", "64k", "512k"]:
        raise ValueError("Invalid resolution. Choose from '16k', '64k', or '512k'.")

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    for object_name in tqdm(YCB_OBJECT_NAMES, desc="Downloading object meshes"):
        url = YCB_DATA_URL + f"google/{object_name}_google_{resolution}.tgz"
        filename = f"{download_dir}/{object_name}.tgz"
        if url_exists(url):
            download_file(url, filename)
            extract_tar_archive(filename, download_dir)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Align meshes to a canonical origin.")
    parser.add_argument("--resolution", type=str, default="16k", help="Resolution of meshes to align.")
    args = parser.parse_args()
    download_ycb_models(resolution=args.resolution)
