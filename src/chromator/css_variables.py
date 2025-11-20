from dataclasses import dataclass
from typing import TYPE_CHECKING

from based_utils.calx import (
    CyclicInterpolationBounds,
    InterpolationBounds,
    fractions,
    interpolate,
)
from based_utils.cli import Colored
from based_utils.colors import Color

if TYPE_CHECKING:
    from collections.abc import Iterator


@dataclass(frozen=True)
class InterpolationParams:
    amount: int = 19
    inclusive: bool = False
    dynamic_range: float = 0


def _colored(s: str, color: Color) -> str:
    return Colored(s, color.contrasting_shade, color).formatted


def _css_color_comment(color: Color) -> str:
    return _colored(f"#{color.hex} --> {color}", color)


def _shades_2(
    c_dark: Color, c_bright: Color, *, params: InterpolationParams
) -> Iterator[Color]:
    dynamic_range = params.dynamic_range
    l_dark = interpolate(dynamic_range, start=c_dark.lightness, end=0)
    l_bright = interpolate(dynamic_range, start=c_bright.lightness, end=1)

    lightness_bounds = InterpolationBounds(l_dark, l_bright)
    saturation_bounds = InterpolationBounds(c_dark.saturation, c_bright.saturation)
    hue_bounds = CyclicInterpolationBounds(c_dark.hue, c_bright.hue)

    for lightness in fractions(params.amount, inclusive=params.inclusive):
        f = lightness_bounds.inverse_interpolate(lightness, inside=False)
        yield Color.from_fields(
            lightness=lightness,
            saturation=saturation_bounds.interpolate(f),
            hue=hue_bounds.interpolate(f),
        )


def shades_as_css_variables(
    c_1: Color, c_2: Color | None, *, params: InterpolationParams, label: str
) -> Iterator[str]:
    if c_2 and c_2 < c_1:
        c_1, c_2 = c_2, c_1

    yield "/*"
    yield "Based on:"

    if c_2:
        yield f"- Darkest:   {_css_color_comment(c_1)}"
        yield f"- Brightest: {_css_color_comment(c_2)}"
        shades = _shades_2(c_1, c_2, params=params)

    else:
        yield _css_color_comment(c_1)
        shades = c_1.shades(params.amount, inclusive=params.inclusive)

    yield "*/"

    for color in shades:
        color_var = f"--{label}-{color.lightness * 100:02.0f}"
        yield _colored(f"{color_var}: #{color.hex}; /* --> {color} */", color)
