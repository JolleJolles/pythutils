# pythutils
**A collection of utility functions for Python**

## Installation

To install pythutils, open a terminal window and enter:
```bash
pip install pythutils
```

## Dependencies
*pythutils* is both Python 2.7 and 3 compatible and has [numpy](http://www.numpy.org/), [pyyaml](https://pyyaml.org), [pandas](https://pandas.pydata.org), and [h5py](https://www.h5py.org) as dependencies that will be automatically installed. Note that this can take very long (up to an hour) with pip on older machines and python versions and faster will be to manually install with `apt-get`.

## Usage
To use the various utility functions, e.g.:

    from pythutils.timeutils import clock
    from pythutils.fileutils import listfiles
    from pythutils.mathutils import points_to_angle
    from pythutils.sysutils import isrpi

## Development
*pythutils* is developed by [Dr Jolle Jolles](http://jollejolles.com) at the Max Planck Institute of Animal Behavior, Konstanz, Germany.

For an overview of version changes see the [CHANGELOG](https://github.com/JolleJolles/pythutils/blob/master/CHANGELOG) and for detailed changes see the [commits page](https://github.com/JolleJolles/pythutils/commits/).

Please submit bugs or feature requests to the GitHub issue tracker [here](https://github.com/JolleJolles/pythutils/issues).

## License
Released under a Apache 2.0 License. See [LICENSE](https://github.com/JolleJolles/pythutils/blob/master/LICENSE) for details.
