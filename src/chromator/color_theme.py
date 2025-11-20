from typing import TYPE_CHECKING

from based_utils.calx import fractions
from based_utils.cli import Colored
from based_utils.colors import COLORS, HUES, Color, Hues

if TYPE_CHECKING:
    from collections.abc import Iterator


def _color_shades(c: Color) -> Iterator[str]:
    for f in fractions(19):
        s = c.shade(f)
        yield Colored(f" {s.hex} ", s.contrasting_shade, s).formatted


def _color_line(c: Color, n: str = "") -> str:
    h = "   " if n == "grey" else f"{c.hue * 360:03.0f}"
    return "".join(_color_shades(c)) + Colored(f" {h} {n}", c).formatted


def _saturation_lines(saturation: float, color_cls: type[Color]) -> Iterator[str]:
    if saturation == 0:
        yield _color_line(color_cls.grey(), "grey")
    else:
        yield "".join(f"   {f * 100:.0f}%  " for f in fractions(19))
        for h in COLORS:
            yield _color_line(color_cls.from_name(h, saturation=saturation), h)


def color_lines(custom_hues: Hues) -> Iterator[str]:
    class CustomColor(Color):
        hues = HUES | custom_hues

    for saturation in fractions(3, inclusive=True):
        yield from _saturation_lines(saturation, CustomColor)
