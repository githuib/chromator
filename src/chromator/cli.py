import argparse
from typing import TYPE_CHECKING

from based_utils.cli import Colored, LogLevel, check_integer_within_range
from based_utils.colors import Color

from . import log
from .shades import InterpolationParams, generate_shades

if TYPE_CHECKING:
    from collections.abc import Iterator

_log = log.get_logger()


def _colored(s: str, color: Color) -> str:
    return Colored(s, color.contrasting_shade, color).formatted


def _css_color_comment(color: Color) -> str:
    return _colored(f"#{color.hex} --> {color}", color)


def _shades_as_css_variables(
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

    for color in generate_shades(c_1, c_2, params=params):
        num = int(color.lightness * 100)
        color_var = f"--{label}-{num:02d}: #{color.hex}; /* --> {color} */"
        yield _colored(color_var, color)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("label", type=str)
    parser.add_argument("-c", "--color1", type=str)
    parser.add_argument("-k", "--color2", type=str, default=None)
    parser.add_argument(
        "-n", "--amount", type=check_integer_within_range(0, None), default=19
    )
    parser.add_argument("-i", "--inclusive", action="store_true", default=False)
    parser.add_argument(
        "-d", "--dynamic-range", type=check_integer_within_range(0, 100), default=0
    )
    args = parser.parse_args()

    with log.context(LogLevel.INFO):
        for line in _shades_as_css_variables(
            Color.from_hex(args.color1),
            Color.from_hex(args.color2),
            params=InterpolationParams(
                args.amount, args.inclusive, args.dynamic_range / 100
            ),
            label=args.label,
        ):
            _log.info(line)
