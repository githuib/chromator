from dataclasses import dataclass

from .color import Color


def c(h: int) -> Color:
    return Color(h / 360)


@dataclass(frozen=True)
class ColorTheme:
    """
    Helper class to make a Colors class return Color objects.

    Can be overridden by specifying a custom anum with
    a different set of hues (in degrees):
    >>> class MyColors(ColorTheme):
    ...     tomato = c(15)
    ...     turquoise = c(175)
    >>> MyColors.tomato
    HSLuv(15.00°, 100.00%, 50.00%)
    >>> MyColors.grey
    HSLuv(0.00°, 0.00%, 50.00%)
    """

    grey = Color(saturation=0)
    black = grey.shade(0)
    white = grey.shade(1)


class Colors(ColorTheme):
    """Highly opinionated (though carefully selected) color theme."""

    red = c(12)
    orange = c(33)
    yellow = c(69)
    poison = c(101)
    green = c(127)
    ocean = c(190)
    blue = c(248)
    indigo = c(267)
    purple = c(281)
    pink = c(329)

    brown = orange.blend(yellow, 0.25).saturated(0.5)


class AltColors(ColorTheme):
    """Alternative color theme."""

    red = c(10)
    orange = c(35)
    yellow = c(75)
    poison = c(100)
    green = c(126)
    ocean = c(184)
    blue = c(242)
    indigo = c(268)
    purple = c(280)
    pink = c(325)

    brown = orange.blend(yellow, 0.3).saturated(0.5)
