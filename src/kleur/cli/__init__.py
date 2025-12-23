from based_utils.cli import run_command

from .palette_gen import ThemeArgsParser
from .shades_gen import CssArgsParser


def main() -> None:
    run_command(ThemeArgsParser, CssArgsParser)
