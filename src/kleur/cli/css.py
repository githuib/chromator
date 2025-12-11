from dataclasses import dataclass
from typing import TYPE_CHECKING

from kleur import Color, Colored
from kleur.interpol import LinearMapping, mapped

from .utils import ArgsParser, check_integer_in_range, print_lines

if TYPE_CHECKING:
    from argparse import Namespace
    from collections.abc import Iterable, Iterator


@dataclass(frozen=True)
class _ShadesParams:
    amount: int = 19
    dynamic_range: float = 0
    include_black_and_white: bool = False
    include_input: bool = False


def _colored(s: str, color: Color) -> str:
    return str(Colored(s, color.contrasting_shade, color))


def _css_color_comment(color: Color) -> str:
    return _colored(f"#{color.as_hex} --> {color}", color)


def _shades(
    input_colors: tuple[Color, Color], shades: Iterable[float], params: _ShadesParams
) -> Iterator[tuple[Color, int]]:
    c_dark, c_bright = input_colors
    old_dark, old_bright = c_dark.lightness, c_bright.lightness
    dark_shade = mapped(params.dynamic_range, (old_dark, 0))
    bright_shade = mapped(params.dynamic_range, (old_bright, 1))
    dark, bright = c_dark.shade(dark_shade), c_bright.shade(bright_shade)
    shade_mapping = LinearMapping(dark_shade, bright_shade)

    def color_for_shade(lightness: float) -> Color:
        return dark.blend(bright, shade_mapping.position_of(lightness))

    for s in shades:
        yield color_for_shade(s), 0

    if params.include_input:
        extra_colors = [color_for_shade(old_dark), color_for_shade(old_bright)]
        if params.dynamic_range:
            extra_colors += [dark, bright]
        for i, c in enumerate(extra_colors, 1):
            yield c, i


def _generate_colors(
    c1: Color, c2: Color | None, params: _ShadesParams
) -> Iterator[tuple[Color, int]]:
    i, n = (0 if params.include_black_and_white else 1), (params.amount + 1)
    shades = [li / n for li in range(i, n + 1 - i)]

    if c2:
        yield from _shades((c1, c2), shades, params)

    else:
        for s in shades:
            yield c1.shade(s), 0
        if params.include_input:
            yield c1, 1


def _css_lines(
    c1: Color, c2: Color | None, colors: Iterable[tuple[Color, int]], label: str
) -> Iterator[str]:
    yield "/*"
    yield "Based on:"
    if c2:
        yield f"- Darkest:   {_css_color_comment(c1)}"
        yield f"- Brightest: {_css_color_comment(c2)}"
    else:
        yield _css_color_comment(c1)
    yield "*/"
    for c, v in colors:
        if v:
            s = " <-- "
            if c2:
                p = "shade" if v in (1, 2) else "hue"
                w = "darkest" if v in (1, 3) else "brightest"
                s += f"same {p} as {w} "
            s += "input"
            c_print = c.contrasting_shade
        else:
            s, c_print = "", c
        var = f"{f'--{label}-{c.lightness * 100:02.0f}'}: #{c.as_hex};"
        comment = f"/* --> {c}{s} */"
        yield _colored(f"{var} {comment}", c_print)


class CssArgsParser(ArgsParser):
    name = "css"

    def _parse_args(self) -> None:
        self._parser.add_argument("-l", "--label", type=str, default="color")
        self._parser.add_argument("-c", "--color1", type=str, required=True)
        self._parser.add_argument("-k", "--color2", type=str)
        self._parser.add_argument(
            "-n", "--amount", type=check_integer_in_range(1, 99), default=19
        )
        self._parser.add_argument(
            "-b", "--include-black-and-white", action="store_true", default=False
        )
        self._parser.add_argument(
            "-i", "--include-input-shades", action="store_true", default=False
        )
        self._parser.add_argument(
            "-d", "--dynamic-range", type=check_integer_in_range(0, 100), default=0
        )

    def _run_command(self, args: Namespace) -> None:
        c1 = Color.from_hex(args.color1)
        if args.color2:
            c2 = Color.from_hex(args.color2)
            if c1 > c2:
                c1, c2 = c2, c1
        else:
            c2 = None
        params = _ShadesParams(
            args.amount,
            args.dynamic_range / 100,
            args.include_black_and_white,
            args.include_input_shades,
        )
        colors = sorted(_generate_colors(c1, c2, params))
        print_lines(_css_lines(c1, c2, colors, args.label))
