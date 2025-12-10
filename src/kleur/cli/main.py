from argparse import ArgumentParser, Namespace

from .css_vars import main as css
from .themes import main as colors


def parse_args(parser: ArgumentParser) -> Namespace:
    subparsers = parser.add_subparsers(required=True)
    css.parse_args(subparsers.add_parser("css"))
    colors.parse_args(subparsers.add_parser("colors"))
    return parser.parse_args()


def main() -> None:
    parser = ArgumentParser()
    args = parse_args(parser)
    args.func(args)
