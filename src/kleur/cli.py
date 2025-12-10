import argparse

from based_utils.cli import LogLevel, check_integer_in_range, parse_key_value_pair
from based_utils.colors import AltColors, Color, Colors, c
from based_utils.data import get_class_vars, try_convert

from . import log
from .color_theme import color_lines
from .css_variables import ShadesParams, shades_as_css_variables

_log = log.get_logger()


def _css_variables(args: argparse.Namespace) -> None:
    with log.context(LogLevel.INFO):
        c1 = Color.from_hex(args.color1)
        c2 = Color.from_hex(args.color2) if args.color2 else None
        params = ShadesParams(
            args.amount,
            args.dynamic_range / 100,
            args.include_black_and_white,
            args.include_input_shades,
        )
        for line in shades_as_css_variables(c1, c2, params=params, label=args.label):
            _log.info(line)


def parse_args_css_variables(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-l", "--label", type=str, default="color")
    parser.add_argument("-c", "--color1", type=str, required=True)
    parser.add_argument("-k", "--color2", type=str)
    parser.add_argument(
        "-n", "--amount", type=check_integer_in_range(0, None), default=19
    )
    parser.add_argument(
        "-b", "--include-black-and-white", action="store_true", default=False
    )
    parser.add_argument(
        "-i", "--include-input-shades", action="store_true", default=False
    )
    parser.add_argument(
        "-d", "--dynamic-range", type=check_integer_in_range(0, 100), default=0
    )
    parser.set_defaults(func=_css_variables)


def _color_theme(args: argparse.Namespace) -> None:
    hues = {k: c(try_convert(int, h, default=333)) for k, h in args.color_hues}
    if args.merge_with_default_theme or not hues:
        theme_cls = AltColors if args.alt_default_theme else Colors
        hues = dict(get_class_vars(theme_cls, Color)) | hues
    with log.context(LogLevel.INFO):
        for line in color_lines(hues, n_shades=args.num_shades):
            _log.info(line)


def parse_args_color_theme(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-c",
        "--color-hues",
        nargs="+",
        metavar="NAME=HUE (1-360)",
        type=parse_key_value_pair,
        default={},
    )
    parser.add_argument(
        "-m", "--merge-with-default-theme", action="store_true", default=False
    )
    parser.add_argument("-a", "--alt-default-theme", action="store_true", default=False)
    parser.add_argument(
        "-n", "--num-shades", type=check_integer_in_range(1, 99), default=19
    )
    parser.set_defaults(func=_color_theme)


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)
    parse_args_css_variables(subparsers.add_parser("css"))
    parse_args_color_theme(subparsers.add_parser("colors"))
    args = parser.parse_args()
    args.func(args)
