from typing import TYPE_CHECKING

from kleur import BLACK, GREY, WHITE, AltColors, Color, Colored, Colors, Highlighter, c
from kleur.interpol import LinearMapping

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


def _perc(s: float) -> str:
    return f"{round(s * 100, 1):n}%"


class LinesGenerator:
    def __init__(self, args: Namespace) -> None:
        ns, nv = args.number_of_shades, args.number_of_vibrances
        self._shades = [s / (ns + 1) for s in range(1, ns + 1)]
        self._vibrances = [v / nv for v in range(1, nv + 1)]

        colors: dict[str, Color] = {}

        if args.merge_with_default_theme or not args.colors:
            # Add colors from default theme.
            theme_cls = AltColors if args.alt_default_theme else Colors
            colors |= get_class_vars(theme_cls, Color)

        # Add custom colors from args.
        for name, hue in args.colors:
            h = try_convert(int, hue, default=333) % 360
            colors[name] = c(h)

        self._colors = dict(sorted(colors.items(), key=lambda i: i[1].hue))
        self._label_length = max(len(n) for n in self._colors) + 6
        # Shades percentages are right above the first color, so let's give them a
        # contrasting hue. Furthermore, making them slightly brighter as the shade
        # increases will give them a more uniform appearance to the human eye.
        self._percentage_color = next(iter(self._colors.values())).contrasting_hue
        # Values based on experimenting with themes differing in starting color.
        # Overall this seems to work well, or at least to my eyes :)
        self._shade_map = LinearMapping(0.6, 0.72)

    def _percentage_columns(self, v: float) -> Iterator[str]:
        cp, sm = self._percentage_color.saturated(v), self._shade_map
        c0 = cp.shade(sm.value_at(0))
        yield Colored(f" {_perc(v)}".ljust(self._label_length), c0.brighter(), c0)

        for s in self._shades:
            yield Colored(" ", bg=cp.shade(s))
            yield Colored(_perc(s).center(7), cp.shade(sm.value_at(s)))

        yield Colored(" ", bg=WHITE)

    def _color_columns(self, name: str, color: Color) -> Iterable[str]:
        hue = f"{color.hue * 360:3.0f}" if color.saturation else ""
        c0 = color.shade(self._shade_map.value_at(0))
        yield Colored(f" {hue:>3} {name}".ljust(self._label_length), c0, BLACK)

        for s in self._shades:
            k = color.shade(s)
            yield Highlighter(k)(k.as_hex.center(8))

        yield Colored(" ", bg=WHITE)

    def _rows(self) -> Iterator[Iterable[str]]:
        yield []
        yield self._percentage_columns(0)
        yield self._color_columns("grey", GREY)
        for v in self._vibrances:
            yield []
            yield self._percentage_columns(v)
            for name, k in self._colors.items():
                ks = k.adjust(saturation=v)
                yield self._color_columns(name, ks)
        yield []

    def lines(self) -> Iterator[str]:
        for columns in self._rows():
            yield "".join(columns)


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
