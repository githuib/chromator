from dataclasses import dataclass
from typing import TYPE_CHECKING

from kleur import Colored
from kleur.interpol import LinearMapping, mapped

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

    from kleur import Color


def _colored(s: str, color: Color) -> str:
    return str(Colored(s, color.contrasting_shade, color))


def _css_color_comment(color: Color) -> str:
    return _colored(f"#{color.as_hex} --> {color}", color)


def _shades(
    input_colors: tuple[Color, Color],
    *,
    dynamic_range: float = 0,
    shades: Iterable[float],
    include_input: bool = False,
) -> list[tuple[Color, int]]:
    c_dark, c_bright = input_colors
    old_dark, old_bright = c_dark.lightness, c_bright.lightness
    dark_shade = mapped(dynamic_range, (old_dark, 0))
    bright_shade = mapped(dynamic_range, (old_bright, 1))
    dark, bright = c_dark.shade(dark_shade), c_bright.shade(bright_shade)
    shade_mapping = LinearMapping(dark_shade, bright_shade)

    def color_for_shade(lightness: float) -> Color:
        return dark.blend(bright, shade_mapping.position_of(lightness))

    colors = [(color_for_shade(s), 0) for s in shades]
    if include_input:
        extra_colors = [color_for_shade(old_dark), color_for_shade(old_bright)]
        if dynamic_range:
            extra_colors += [dark, bright]
        colors += [(c, i) for i, c in enumerate(extra_colors, 1)]
    return sorted(colors)


@dataclass(frozen=True)
class ShadesParams:
    amount: int = 19
    dynamic_range: float = 0
    include_black_white: bool = False
    include_input: bool = False


def _generate_colors(
    c1: Color, c2: Color | None, params: ShadesParams
) -> list[tuple[Color, int]]:
    s, n = (0 if params.include_black_white else 1), (params.amount + 1)
    shades = [li / n for li in range(s, n + 1 - s)]

    if c2:
        return _shades(
            (c1, c2),
            dynamic_range=params.dynamic_range,
            include_input=params.include_input,
            shades=shades,
        )

    colors = [(c1.shade(s), 0) for s in shades]
    if params.include_input:
        colors.append((c1, 1))
    return sorted(colors)


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


def shades_as_css_variables(
    c1: Color, c2: Color | None, *, params: ShadesParams, label: str
) -> Iterator[str]:
    if c2 and c1 > c2:
        c1, c2 = c2, c1
    yield from _css_lines(c1, c2, _generate_colors(c1, c2, params), label)
