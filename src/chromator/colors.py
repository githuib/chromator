from collections.abc import Iterator
from dataclasses import dataclass
from functools import cached_property
from math import pi

HSLuv = tuple[float, float, float]


def trim(n: float, lower: float, upper: float):
    return min(max(lower, n), upper)


@dataclass
class Bounds:
    lower: float
    upper: float

    @cached_property
    def span(self):
        return self.upper - self.lower

    def interpolate(self, f: float):
        return self.lower + self.span * f

    def inverse_interpolate(self, n: float, inside=True):
        try:
            f = (n - self.lower) / self.span
        except ZeroDivisionError:
            return 0.0
        return trim(f, 0.0, 1.0) if inside else f


class CyclicBounds(Bounds):
    def __init__(self, lower: float, upper: float, period: float = pi * 2):
        lower = lower % period
        upper = upper % period
        span = upper - lower
        if span > period / 2:
            lower += period
        if span < -period / 2:
            upper += period

        super().__init__(lower, upper)
        self.period = period

    def interpolate(self, f: float):
        return super().interpolate(f) % self.period

    def inverse_interpolate(self, n: float, inside=True):
        return super().inverse_interpolate(n % self.period, inside)


def contrasting_color(color: HSLuv) -> HSLuv:
    hue, saturation, lightness = color
    return hue, saturation, (lightness + 50) % 100


def shades_1(
    color: HSLuv,
    step: int = 5,
    inclusive: bool = False,
) -> Iterator[HSLuv]:
    hue, saturation, _ = color
    s = step if inclusive else 0
    for lightness in range(step - s, 100 + s, step):
        yield hue, saturation, lightness


def shades_2(
    color_1: HSLuv,
    color_2: HSLuv,
    step: int = 5,
    extrapolate: float = 0,
    inclusive: bool = False,
) -> Iterator[HSLuv]:
    _, _, l_1 = color_1
    _, _, l_2 = color_2
    if l_1 > l_2:
        color_1, color_2 = color_2, color_1
    h_1, s_1, l_1 = color_1
    h_2, s_2, l_2 = color_2

    l_1 = Bounds(l_1, 0).interpolate(extrapolate)
    l_2 = Bounds(l_2, 100).interpolate(extrapolate)

    hue_bounds = CyclicBounds(h_1, h_2, 360)
    saturation_bounds = Bounds(s_1, s_2)
    lightness_bounds = Bounds(l_1, l_2)

    s = step if inclusive else 0
    for lightness in range(step - s, 100 + s, step):
        f = lightness_bounds.inverse_interpolate(lightness)
        hue = hue_bounds.interpolate(f)
        saturation = saturation_bounds.interpolate(f)
        yield hue, saturation, lightness


def shades(
    color_1: HSLuv,
    color_2: HSLuv = None,
    step: int = 5,
    extrapolate: float = 0,
    inclusive: bool = False,
):
    if color_2:
        yield from shades_2(color_1, color_2, step, extrapolate, inclusive)
    else:
        yield from shades_1(color_1, step, inclusive)
