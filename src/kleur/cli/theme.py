from typing import TYPE_CHECKING

from kleur import AltColors, Color, Colored, Colors, ColorTheme, c

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


def _color_shade(color: Color) -> str:
    return f"{Colored(color.as_hex.center(8), color.contrasting_shade, color)}"


def _color_line(color: Color, name: str, shades: Iterable[float]) -> str:
    shades_str = "".join(_color_shade(color.shade(s)) for s in shades)
    hue = "   " if name == "grey" else f"{color.hue * 360:03.0f}"
    return f"{shades_str}{Colored(f' {hue} {name}', color)}"


def _color_lines(
    color_theme: dict[str, Color], n_shades: int, n_sats: int
) -> Iterator[str]:
    n = n_shades + 1
    shades = [i / n for i in range(1, n)]

    # Any color will be grey when saturation is set to 0.
    yield _color_line(ColorTheme.grey, "grey", shades)

    # Shade/hue tables for specific saturation values
    for i in range(1, n_sats + 1):
        # Shade percentages row
        yield "".join(f"{s:.2%}".center(8) for s in shades)
        # Tables
        saturation = i / n_sats
        for name, color in sorted(color_theme.items(), key=lambda p: p[1].hue):
            yield _color_line(color.adjust(saturation=saturation), name, shades)


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
        hues = {k: c(try_convert(int, h, default=333)) for k, h in args.colors}
        if args.merge_with_default_theme or not hues:
            theme_cls = AltColors if args.alt_default_theme else Colors
            hues = dict(get_class_vars(theme_cls, Color)) | hues
        print_lines(_color_lines(hues, args.number_of_shades, args.number_of_vibrances))
