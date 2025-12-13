from typing import TYPE_CHECKING

from kleur import AltColors, Color, Colored, Colors

from .utils import (
    ArgsParser,
    check_integer_in_range,
    get_class_vars,
    parse_key_value_pair,
    print_lines,
    try_convert,
)

if TYPE_CHECKING:
    from argparse import Namespace
    from collections.abc import Iterable, Iterator

BLOCK_WIDTH = 8


class LinesGenerator:
    def __init__(self, args: Namespace) -> None:
        n_shades, n_vibrances = args.number_of_shades, args.number_of_vibrances
        self._shades = [s / (n_shades + 1) for s in range(1, n_shades + 1)]
        self._vibrances = [v / n_vibrances for v in range(1, n_vibrances + 1)]

        hues: dict[int, str] = {}

        if args.merge_with_default_theme or not args.colors:
            theme_cls = AltColors if args.alt_default_theme else Colors
            for name, color in get_class_vars(theme_cls, Color).items():
                hues[round(color.hue * 360)] = name

        for name, hue in args.colors:
            hues[try_convert(int, hue, default=333)] = name

        self._hues = sorted(hues.items())

    def _blocks(
        self, name: str, vibrance: float, hue: float = None
    ) -> Iterable[Colored]:
        color = Color(hue or 0, vibrance)

        for s in self._shades:
            c = color.shade(s)
            yield Colored(c.as_hex.center(BLOCK_WIDTH), c.contrasting_shade, c)

        hue_str = "   " if hue is None else f"{hue * 360:03.0f}"
        yield Colored(f" {hue_str} {name}", color)

    def _line(self, name: str, vibrance: float, hue: float = None) -> str:
        return "".join(str(c) for c in self._blocks(name, vibrance, hue))

    def lines(self) -> Iterator[str]:
        yield self._line("grey", 0)

        for vibrance in self._vibrances:
            yield "".join(f"{s:.2%}".center(BLOCK_WIDTH) for s in self._shades)

            for hue, name in self._hues:
                yield self._line(name, vibrance, hue / 360)


class ThemeArgsParser(ArgsParser):
    name = "theme"

    def _parse_args(self) -> None:
        self._parser.add_argument(
            "-c",
            "--colors",
            nargs="+",
            metavar="NAME=HUE (1-360)",
            type=parse_key_value_pair,
            default={},
        )
        self._parser.add_argument(
            "-m", "--merge-with-default-theme", action="store_true", default=False
        )
        self._parser.add_argument(
            "-a", "--alt-default-theme", action="store_true", default=False
        )
        self._parser.add_argument(
            "-s", "--number-of-shades", type=check_integer_in_range(1, 99), default=9
        )
        self._parser.add_argument(
            "-v", "--number-of-vibrances", type=check_integer_in_range(1, 99), default=2
        )

    def _run_command(self, args: Namespace) -> None:
        print_lines(LinesGenerator(args).lines())
