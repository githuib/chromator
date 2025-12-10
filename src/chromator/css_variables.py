from dataclasses import dataclass
from typing import TYPE_CHECKING

from based_utils.calx import LinearMapping, fractions, mapped
from based_utils.cli import Colored

if TYPE_CHECKING:
    from collections.abc import Iterator

    from based_utils.colors import Color


def _colored(s: str, color: Color) -> str:
    return str(Colored(s, color.contrasting_shade, color))


def _css_color_comment(color: Color) -> str:
    return _colored(f"#{color.as_hex} --> {color}", color)


@dataclass(frozen=True)
class ShadesParams:
    amount: int = 19
    dynamic_range: float = 0
    include_black_white: bool = False
    include_input: bool = False


def _shades(
    c_dark: Color, c_bright: Color, *, params: ShadesParams
) -> list[tuple[Color, int]]:
    old_dark, old_bright = c_dark.lightness, c_bright.lightness
    dark_shade = mapped(params.dynamic_range, (old_dark, 0))
    bright_shade = mapped(params.dynamic_range, (old_bright, 1))
    dark, bright = c_dark.shade(dark_shade), c_bright.shade(bright_shade)
    shade_mapping = LinearMapping(dark_shade, bright_shade)

    def color_for_li(lightness: float) -> Color:
        return dark.blend(bright, shade_mapping.position_of(lightness))

    shades = fractions(params.amount, inclusive=params.include_black_white)
    colors = [(color_for_li(li), 0) for li in shades]
    if params.include_input:
        colors += [(color_for_li(old_dark), 1), (color_for_li(old_bright), 2)]
    return sorted(colors)


def shades_as_css_variables(
    c_1: Color, c_2: Color | None, *, params: ShadesParams, label: str
) -> Iterator[str]:
    yield "/*"
    yield "Based on:"

    if c_2:
        if c_2 < c_1:
            c_1, c_2 = c_2, c_1

        yield f"- Darkest:   {_css_color_comment(c_1)}"
        yield f"- Brightest: {_css_color_comment(c_2)}"
        shades = _shades(c_1, c_2, params=params)

    else:
        yield _css_color_comment(c_1)
        shades = [
            (c_1.shade(s), 0)
            for s in fractions(params.amount, inclusive=params.include_black_white)
        ]
        if params.include_input:
            shades.append((c_1, 1))
        shades.sort()

    yield "*/"

    for c, v in shades:
        if v:
            s = " <-- "
            if c_2:
                s += f"same lightness as {'darkest' if v == 1 else 'brightest'} "
            s += "input"
            c_print = c.contrasting_shade

        else:
            s, c_print = "", c

        var = f"{f'--{label}-{c.lightness * 100:02.0f}'}: #{c.as_hex};"
        comment = f"/* --> {c}{s} */"
        yield _colored(f"{var} {comment}", c_print)
