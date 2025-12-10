from typing import TYPE_CHECKING

from kleur import Color, Colored, ColorTheme

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator


def _color_shade(color: Color) -> str:
    return f"{Colored(color.as_hex.center(8), color.contrasting_shade, color)}"


def _color_line(color: Color, name: str, shades: Iterable[float]) -> str:
    shades_str = "".join(_color_shade(color.shade(s)) for s in shades)
    hue = "   " if name == "grey" else f"{color.hue * 360:03.0f}"
    return f"{shades_str}{Colored(f' {hue} {name}', color)}"


def color_lines(color_theme: dict[str, Color], *, n_shades: int = 19) -> Iterator[str]:
    n = n_shades + 1
    shades = [i / n for i in range(1, n)]

    # Any color will be grey when saturation is set to 0.
    yield _color_line(ColorTheme.grey, "grey", shades)

    # Shade/hue tables for specific saturation values
    num_saturations = 4
    for i in range(1, num_saturations + 1):
        # Shade percentages row
        yield "".join(f"{s:.2%}".center(8) for s in shades)
        # Tables
        saturation = i / num_saturations
        for name, color in sorted(color_theme.items(), key=lambda p: p[1].hue):
            yield _color_line(color.adjust(saturation=saturation), name, shades)
