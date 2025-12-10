from typing import TYPE_CHECKING

from kleur import Color
from kleur.cli.utils import check_integer_in_range, print_lines

from .css_variables import ShadesParams, shades_as_css_variables

if TYPE_CHECKING:
    from argparse import ArgumentParser, Namespace


def _css_variables(args: Namespace) -> None:
    c1 = Color.from_hex(args.color1)
    c2 = Color.from_hex(args.color2) if args.color2 else None
    params = ShadesParams(
        args.amount,
        args.dynamic_range / 100,
        args.include_black_and_white,
        args.include_input_shades,
    )
    print_lines(shades_as_css_variables(c1, c2, params=params, label=args.label))


def parse_args(parser: ArgumentParser) -> None:
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
