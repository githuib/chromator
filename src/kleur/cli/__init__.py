import sys

from .palette_gen import PaletteGenerator
from .shades_gen import ShadesGenerator

try:
    from based_utils.cli import run_command
except ImportError:
    run_command = None


def main() -> None:
    if run_command:
        run_command(PaletteGenerator, ShadesGenerator)
    else:
        sys.exit("Install package as 'kleur[cli]' to use any console scripts in ot.")
