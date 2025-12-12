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
) -> Iterator[tuple[Color, str]]:
    """Generate shades of a color."""
    for s in shades:
        yield input_color.shade(s), ""
    if include_input:
        yield input_color, "input"


def _shades_2(
    input_colors: tuple[Color, Color],
    shades: Iterable[float],
    dynamic_range: float,
    include_input: bool,  # noqa: FBT001
) -> Iterator[tuple[Color, str]]:
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
        yield color_for_shade(s), ""

    if include_input:

        def _input_indication(extreme: str, prop: str) -> str:
            return f"same {prop} as {extreme} input"

        yield color_for_shade(old_dark), _input_indication("darkest", "shade")
        yield color_for_shade(old_bright), _input_indication("brightest", "shade")
        if dynamic_range:
            yield dark, _input_indication("darkest", "hue")
            yield bright, _input_indication("brightest", "hue")


def _colored(s: str, color: Color) -> str:
    return str(Colored(s, color.contrasting_shade, color))


def _css_color_comment(color: Color) -> str:
    return _colored(f"#{color.as_hex} --> {color}", color)


def _lines(args: Namespace) -> Iterator[str]:
    inc_i = args.include_input_shades
    s, b = args.number_of_shades, 0 if args.include_black_and_white else 1
    shades = [li / (s + 1) for li in range(b, s + 2 - b)]
    c1 = Color.from_hex(args.color1)
    yield "/*"
    yield "Based on:"
    if not args.color2:
        yield _css_color_comment(c1)
        colors = _shades_1(c1, shades, inc_i)
    else:
        c2 = Color.from_hex(args.color2)
        if c1 > c2:
            c1, c2 = c2, c1
        yield f"- Darkest:   {_css_color_comment(c1)}"
        yield f"- Brightest: {_css_color_comment(c2)}"
        colors = _shades_2((c1, c2), shades, args.dynamic_range / 100, inc_i)
    yield "*/"
    for c, input_indication in sorted(colors):
        var = f"{f'--{args.label}-{c.lightness * 100:02.0f}'}: #{c.as_hex};"
        extra = f" <-- {input_indication}" if input_indication else ""
        c_print = c.contrasting_shade if input_indication else c
        yield _colored(f"{var} /* --> {c}{extra} */", c_print)


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
        print_lines(_lines(args))
