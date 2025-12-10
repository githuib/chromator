from typing import TYPE_CHECKING

from kleur import AltColors, Color, Colors, c
from kleur.cli.utils import (
    check_integer_in_range,
    get_class_vars,
    parse_key_value_pair,
    print_lines,
    try_convert,
)

from .color_theme import color_lines

if TYPE_CHECKING:
    from argparse import ArgumentParser, Namespace


def _color_theme(args: Namespace) -> None:
    hues = {k: c(try_convert(int, h, default=333)) for k, h in args.color_hues}
    if args.merge_with_default_theme or not hues:
        theme_cls = AltColors if args.alt_default_theme else Colors
        hues = dict(get_class_vars(theme_cls, Color)) | hues
    print_lines(color_lines(hues, n_shades=args.num_shades))


def parse_args(parser: ArgumentParser) -> None:
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
