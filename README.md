# 🔧 YCB Converter
This repository provides tools to convert [YCB (Yale-Carnegie Mellon-Berkeley) Objects](https://www.ycbbenchmarks.com/) into formats usable in rigid body physics simulation.
Running the main script will download YCB models and convert them to simulation-ready URDF models (and optionally to USD if a path to Isaac Orbit is set):
```bash
python ycb_converter/main.py --orbit-path /path/to/orbit
```


## Requirements
- [`coacd`](https://github.com/SarahWeiii/CoACD) -  for convex decomposition
- [`trimesh`](https://trimesh.org/) - for mesh manipulation
- [`yourdfpy`](https://yourdfpy.readthedocs.io/en/latest/) - for URDF generation
- ([`orbit`](https://isaac-orbit.github.io/)-  for USD conversion)

Required dependencies (except for Isaac ORBIT) can be installed via `pip install -r requirements.txt`.
To install ORBIT, follow the instructions on the [official website](https://isaac-orbit.github.io/).

## Features
To understand and inspect the different stages of the conversion process, go to the [Quickstart Notebook](./notebooks/quickstart.ipynb).

The object weights in [`data/weights.json`](./data/weights.json) were determined using a scale for all objects for which there are laser scans.

[//]: # (Functionalities relating to different stages of the conversion process are provided in separate scripts.)

[//]: # (1. [`download_ycb_models`]&#40;./ycb_converter/download_ycb_models.py&#41; - Downloads OBJ models from the official website.)

[//]: # (2. [`align_to_origin`]&#40;./ycb_converter/align_to_origin.py&#41; - Aligns the models to a canonical origin.)

[//]: # (3. [`convex_decompose`]&#40;./ycb_converter/convex_decompose.py&#41; - Decomposes the models into convex parts.)

[//]: # (4. [`assemble_urdf`]&#40;./ycb_converter/assemble_urdf.py&#41; - Assembles meshes and inertial properties into a URDF model.)

[//]: # (5. [`convert_to_usd`]&#40;./ycb_converter/convert_to_usd.py&#41; - Converts the URDF model to USD format.)
