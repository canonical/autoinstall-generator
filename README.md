
# autoinstall-generator

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/autoinstall-generator)

Objective: Ingest Debian preseed format file(s), and provide compatible
Subiquity autoinstall in response.

Project Status: First public release.  Some basic support is present but there
is room for improvement.  Several directive types have only partial support,
including network.  Partition handling is very basic and only identifies 'lvm'
or 'normal' types.  Pre/post command support not yet handled.

## Usage

    usage: autoinstall-generator.py [-h] [-c] [-d] [-V] infile [outfile]

    positional arguments:
      infile         Debian install preseed file, or a dash to read stdin
      outfile        Subiquity autoinstall yaml

    optional arguments:
      -h, --help     show this help message and exit
      -c, --cloud    output in cloud-config format
      -d, --debug    include commented out debug output explaining the conversions
                     performed
      -V, --version  show version and exit

## Feedback

Please direct bugs and feature requests to the project on
[Launchpad](https://bugs.launchpad.net/autoinstall-generator/+filebug).
