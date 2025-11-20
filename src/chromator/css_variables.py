from dataclasses import dataclass
from typing import TYPE_CHECKING

from based_utils.calx import (
    CyclicInterpolationBounds,
    InterpolationBounds,
    fractions,
    interpolate,
    trim,
)
from based_utils.cli import Colored
from based_utils.colors import Color

from . import log

if TYPE_CHECKING:
    from collections.abc import Iterator


_log = log.get_logger()


@dataclass(frozen=True)
class InterpolationParams:
    n: int = 19
    inclusive: bool = False
    dynamic_range: float = 0


def _shades_2(
    color_1: Color, color_2: Color, *, params: InterpolationParams
) -> Iterator[Color]:
    c_dark, c_bright = sorted([color_1, color_2])

    dynamic_range = params.dynamic_range
    l_dark = interpolate(dynamic_range, start=c_dark.lightness, end=0)
    l_bright = interpolate(dynamic_range, start=c_bright.lightness, end=1)
    lightness_bounds = InterpolationBounds(l_dark, l_bright)

    saturation_bounds = InterpolationBounds(c_dark.saturation, c_bright.saturation)
    hue_bounds = CyclicInterpolationBounds(c_dark.hue, c_bright.hue)

    for lightness in fractions(params.n, inclusive=params.inclusive):
        f = lightness_bounds.inverse_interpolate(lightness, inside=False)
        hue = hue_bounds.interpolate(f)
        saturation = trim(saturation_bounds.interpolate(f))
        yield Color(lightness, saturation, hue)


def _generate_shades(
    color_1: Color, color_2: Color = None, *, params: InterpolationParams
) -> Iterator[Color]:
    return (
        _shades_2(color_1, color_2, params=params)
        if color_2
        else color_1.shades(params.n, inclusive=params.inclusive)
    )


def _colored(s: str, color: Color) -> str:
    return Colored(s, color.contrasting_shade, color).formatted


def _css_color_comment(color: Color) -> str:
    return _colored(f"#{color.hex} --> {color}", color)


def shades_as_css_variables(
    c_1: Color, c_2: Color | None, *, params: InterpolationParams, label: str
) -> Iterator[str]:
    yield "/*"
    yield "Based on:"
    if c_2:
        c_dark, c_bright = sorted([c_1, c_2])
        yield f"- Darkest:   {_css_color_comment(c_dark)}"
        yield f"- Brightest: {_css_color_comment(c_bright)}"
    else:
        yield _css_color_comment(c_1)
    yield "*/"

    for color in _generate_shades(c_1, c_2, params=params):
        num = int(color.lightness * 100)
        color_var = f"--{label}-{num:02d}: #{color.hex}; /* --> {color} */"
        yield _colored(color_var, color)
