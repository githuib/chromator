import argparse

from based_utils.cli import LogLevel, check_integer_within_range
from based_utils.colors import HUES, Color

from . import log
from .color_theme import color_lines
from .css_variables import InterpolationParams, shades_as_css_variables

_log = log.get_logger()


def css_variables(args: argparse.Namespace) -> None:
    with log.context(LogLevel.INFO):
        for line in shades_as_css_variables(
            Color.from_hex(args.color1),
            Color.from_hex(args.color2),
            params=InterpolationParams(
                args.amount, args.inclusive, args.dynamic_range / 100
            ),
            label=args.label,
        ):
            _log.info(line)


def color_theme(args: argparse.Namespace) -> None:
    with log.context(LogLevel.INFO):
        for line in color_lines(
            {h: v for h in HUES if (v := getattr(args, h)) is not None}
        ):
            _log.info(line)


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    parser_css_variables = subparsers.add_parser("css")
    parser_css_variables.add_argument("label", type=str)
    parser_css_variables.add_argument("-c", "--color1", type=str)
    parser_css_variables.add_argument("-k", "--color2", type=str, default=None)
    parser_css_variables.add_argument(
        "-n", "--amount", type=check_integer_within_range(0, None), default=19
    )
    parser_css_variables.add_argument(
        "-i", "--inclusive", action="store_true", default=False
    )
    parser_css_variables.add_argument(
        "-d", "--dynamic-range", type=check_integer_within_range(0, 100), default=0
    )
    parser_css_variables.set_defaults(func=css_variables)

    parser_color_theme = subparsers.add_parser("colors")
    for color in HUES:
        parser_color_theme.add_argument(f"--{color}", dest=color, type=int)
    parser_color_theme.set_defaults(func=color_theme)

    args = parser.parse_args()
    args.func(args)
