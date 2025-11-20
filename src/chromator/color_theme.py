from typing import TYPE_CHECKING

from based_utils.calx import fractions
from based_utils.cli import Colored
from based_utils.colors import HUES, Color, Hues

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator


def _color_shade(color: Color) -> str:
    return Colored(f" {color.hex} ", color.contrasting_shade, color).formatted


def _color_line(color: Color, name: str, shades: Iterable[float]) -> str:
    shades_str = "".join(_color_shade(color.shade(s)) for s in shades)
    hue = "   " if name == "grey" else f"{color.hue * 360:03.0f}"
    return shades_str + Colored(f" {hue} {name}", color).formatted


def color_lines(custom_hues: Hues) -> Iterator[str]:
    class CustomColor(Color):
        hues = HUES | custom_hues

    shades = list(fractions(19))

    # Any color will be grey when saturation is set to 0.
    yield _color_line(CustomColor.grey(), "grey", shades)

    # Shade/hue tables for specific saturation values
    num_saturations = 4
    for i in range(1, num_saturations + 1):
        # Shade percentages row
        yield "".join(f"   {s * 100:.0f}%  " for s in shades)
        # Tables
        saturation = i / num_saturations
        for name in HUES:
            color = CustomColor.from_name(name, saturation=saturation)
            yield _color_line(color, name, shades)
