# OpenTimelineIO SVG Adapter
[![Build Status](https://github.com/OpenTimelineIO/otio-svg-adapter/actions/workflows/ci.yaml/badge.svg)](https://github.com/OpenTimelineIO/otio-svg-adapter/actions/workflows/ci.yaml)
![Dynamic YAML Badge](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FOpenTimelineIO%2Fotio-svg-adapter%2Fmain%2F.github%2Fworkflows%2Fci.yaml&query=%24.jobs%5B%22test-plugin%22%5D.strategy.matrix%5B%22otio-version%22%5D&label=OpenTimelineIO)
![Dynamic YAML Badge](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FOpenTimelineIO%2Fotio-svg-adapter%2Fmain%2F.github%2Fworkflows%2Fci.yaml&query=%24.jobs%5B%22test-plugin%22%5D.strategy.matrix%5B%22python-version%22%5D&label=Python)

The `svg` adapter is part of OpenTimelineIO's core adapter plugins.  
It renders a svg representation of an otio file.  
Points in calculations are y-up. Points in SVG are y-down.

# Adapter Feature Matrix

The following features of OTIO are supported by the `svg` adapter:

|Feature                  | Support |
|-------------------------|:-------:|
|Single Track of Clips    |    ✔    |
|Multiple Video Tracks    |    ✔    |
|Audio Tracks & Clips     |    ✔    |
|Gap/Filler               |    ✔    |
|Markers                  |    ✔    |
|Nesting                  |    ✖    |
|Transitions              |    ✔    |
|Audio/Video Effects      |   N/A   |
|Linear Speed Effects     |   N/A   |
|Fancy Speed Effects      |   N/A   |
|Color Decision List      |   N/A   |
|Image Sequence Reference |    ✔    |

# Adapter specific arguments
The svg adapter adds a couple of optional arguments to the `write_to_string()` function to set the 
size of the rendered image
>write_to_string(input_otio, **width=2406.0**, **height=1054.0**)

# License
OpenTimelineIO and the "svg" adapter are open source software. 
Please see the [LICENSE](LICENSE) for details.

Nothing in the license file or this project grants any right to use Pixar or 
any other contributor’s trade names, trademarks, service marks, or product names.

# Build instructions

We use uv for development and testing. See the uv [installation instructions](https://docs.astral.sh/uv/#installation)
if you don't already have it installed.

Getting started is simple:

```bash
# install the project's dependencies and create/update the virtual environment
uv sync
```

To verify the adapter is working, run a conversion:

```bash
uv run otioconvert -i sample.otio -o sample.svg
```

If this succeeds, `otioconvert` will use the adapter from your local checkout.

### Troubleshooting tips

If uv is selecting an incompatible Python version, you can pin the project to a supported version:

```bash
# pin the Python interpreter version for the current project
uv python pin 3.12
```

```bash
# install the project's dependencies and create/update the virtual environment
uv sync
```

```bash
# run otioconvert 
uv run otioconvert -i sample.otio -o sample.svg
```

The `.python-version` file records the Python version for the project, while `uv.lock` records the resolved dependency versions. Keeping these files in the repository helps provide a consistent development environment across machines.

# Contributions

If you want to contribute to the project, 
please see: https://opentimelineio.readthedocs.io/en/latest/tutorials/contributing.html  
Please also read up on [testing your code](https://github.com/OpenTimelineIO/otio-plugin-template#testing-your-plugin-during-development) 
in the "getting started" section of the OpenTimelineIO plugin template repository.

# Contact

For more information, please visit http://opentimeline.io/
or https://github.com/AcademySoftwareFoundation/OpenTimelineIO
or join our discussion forum: https://lists.aswf.io/g/otio-discussion
