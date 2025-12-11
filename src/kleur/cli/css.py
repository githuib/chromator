from typing import TYPE_CHECKING

from kleur import Color, Colored
from kleur.interpol import LinearMapping, mapped

from .utils import ArgsParser, check_integer_in_range, print_lines

if TYPE_CHECKING:
    from argparse import Namespace
    from collections.abc import Iterable, Iterator


def _shades_1(
    input_color: Color,
    shades: Iterable[float],
    include_input: bool,  # noqa: FBT001
) -> Iterator[tuple[Color, int]]:
    """Generate shades of a color."""
    for s in shades:
        yield input_color.shade(s), 0
    if include_input:
        yield input_color, 1


def _shades_2(
    input_colors: tuple[Color, Color],
    shades: Iterable[float],
    dynamic_range: float,
    include_input: bool,  # noqa: FBT001
) -> Iterator[tuple[Color, int]]:
    """
    Generate shades based on two colors.

    The dynamic range specifies to what degree the hue
    of the input colors will be used as boundaries:
    - dynamic range 0 (0%):
        The shades will interpolate (or extrapolate) between the input colors
    - dynamic range between 0 and 1 (between 0% and 100%):
        The shades will interpolate (or extrapolate) between
        darker / brighter shades of the input colors
    - dynamic range 1 (100%):
        The shades will interpolate (or extrapolate) between
        the darkest & brightest shades of the input colors
    """
    c_dark, c_bright = input_colors
    old_dark, old_bright = c_dark.lightness, c_bright.lightness
    dark_shade = mapped(dynamic_range, (old_dark, 0))
    bright_shade = mapped(dynamic_range, (old_bright, 1))
    dark, bright = c_dark.shade(dark_shade), c_bright.shade(bright_shade)
    shade_mapping = LinearMapping(dark_shade, bright_shade)

    def color_for_shade(lightness: float) -> Color:
        return dark.blend(bright, shade_mapping.position_of(lightness))

    for s in shades:
        yield color_for_shade(s), 0

    if include_input:
        extra_colors = [color_for_shade(old_dark), color_for_shade(old_bright)]
        if dynamic_range:
            extra_colors += [dark, bright]
        for i, c in enumerate(extra_colors, 1):
            yield c, i


def _colored(s: str, color: Color) -> str:
    return str(Colored(s, color.contrasting_shade, color))


def _css_color_comment(color: Color) -> str:
    return _colored(f"#{color.as_hex} --> {color}", color)


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
            "-s", "--number-of-shades", type=check_integer_in_range(1, 99), default=19
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

        inc_i, inc_bw = args.include_input_shades, args.include_black_and_white
        s, i, d = (args.number_of_shades, 0 if inc_bw else 1, args.dynamic_range / 100)
        shades = [li / (s + 1) for li in range(i, s + 2 - i)]
        colors = (
            _shades_1(c1, shades, inc_i)
            if not c2
            else _shades_2((c1, c2), shades, d, inc_i)
        )
        print_lines(_css_lines(c1, c2, sorted(colors), args.label))
