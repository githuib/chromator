from .colors import ColorsArgsParser
from .css import CssArgsParser
from .utils import run_command


def main() -> None:
    run_command(ColorsArgsParser, CssArgsParser)
