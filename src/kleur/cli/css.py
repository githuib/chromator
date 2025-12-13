from abc import ABC, abstractmethod
from math import log10
from typing import TYPE_CHECKING

from kleur import Color, Colored
from kleur.interpol import LinearMapping, mapped

from .utils import ArgsParser, check_integer_in_range, print_lines

if TYPE_CHECKING:
    from argparse import Namespace
    from collections.abc import Iterator


def _css_color_comment(color: Color) -> Colored:
    return Colored(f"#{color.as_hex} --> {color}", color, color.contrasting_shade)


class LinesGenerator(ABC):
    def __init__(self, args: Namespace) -> None:
        self._include_input = args.include_input_shades
        self._include_bw = args.include_black_and_white
        self._label = args.label
        steps = args.number_of_shades + 1
        shades_range = (0, steps + 1) if self._include_bw else (1, steps)
        self._shades = [s / steps for s in range(*shades_range)]
        self._generated_shades: set[int] = set()

    @abstractmethod
    def _comment_lines(self) -> Iterator[str]: ...

    @abstractmethod
    def _colors(self) -> Iterator[tuple[Color, str]]: ...

    def lines(self) -> Iterator[str]:
        yield "/*"
        yield from self._comment_lines()
        yield "*/"

        colors = {round(c.lightness * 100): (c, i) for c, i in self._colors()}
        sorted_colors = sorted(colors.items())
        s_max, _ = sorted_colors[-1]
        n_digits = int(log10(s_max)) + 1
        for s, (c, input_indication) in sorted_colors:
            css_var = f"--{self._label}-{str(s).zfill(n_digits)}: #{c.as_hex};"
            i = f" <-- {input_indication}" if input_indication else ""
            line = f"{css_var} /* --> {c}{i} */"
            k = c.contrasting_shade
            yield str(Colored(line, *((c, k) if input_indication else (k, c))))


class LinesGeneratorOneColor(LinesGenerator):
    def __init__(self, args: Namespace) -> None:
        super().__init__(args)
        self._input_color = Color.from_hex(args.color1)

    def _comment_lines(self) -> Iterator[str]:
        yield f"Based on: {_css_color_comment(self._input_color)}"

    def _colors(self) -> Iterator[tuple[Color, str]]:
        """Generate shades of a color."""
        for s in self._shades:
            yield self._input_color.shade(s), ""

        if self._include_input:
            yield self._input_color, "input"


def normalize_color(c1: Color, c2: Color) -> Color:
    return c1 if round(c1.saturation, 2) else c1.shifted(c2.hue)


class LinesGeneratorTwoColors(LinesGenerator):
    def __init__(self, args: Namespace) -> None:
        super().__init__(args)
        self._dynamic_range = args.dynamic_range / 100
        c1, c2 = Color.from_hex(args.color1), Color.from_hex(args.color2)
        c1 = normalize_color(c1, c2)
        c2 = normalize_color(c2, c1)
        self._input_colors = sorted((c1, c2))

    def _comment_lines(self) -> Iterator[str]:
        dark, bright = [_css_color_comment(c) for c in self._input_colors]
        yield "Based on:"
        yield f"- Darkest:   {dark}"
        yield f"- Brightest: {bright}"

    def _colors(self) -> Iterator[tuple[Color, str]]:
        """
        Generate shades based on two colors.

        The dynamic range specifies to what degree the hue
        of the input colors will be used as boundaries:
        - dynamic range 0 (0%):
            The shades will interpolate (or extrapolate) between the input colors
        - dynamic range between 0 and 1 (between 0% and 100%):
            The shades will interpolate (or extrapolate) between
            darker / brighter shades of the input colors
        - dynamic range 1 (100%):
            The shades will interpolate (or extrapolate) between
            the darkest & brightest shades of the input colors
        """
        dark, bright = mapping_colors = [
            c.shade(mapped(self._dynamic_range, (c.lightness, i)))
            for i, c in enumerate(self._input_colors)
        ]
        shade_mapping = LinearMapping(dark.lightness, bright.lightness)

        def blend(lightness: float) -> Color:
            return dark.blend(bright, shade_mapping.position_of(lightness))

        for s in self._shades:
            yield blend(s), ""

        if self._include_input:
            sides = "darkest", "brightest"
            for side, old, new in zip(
                sides, self._input_colors, mapping_colors, strict=True
            ):
                if old != new:
                    yield new, f"same hue & saturation as {side} input"
                prop = "color" if old == new else "shade"
                yield blend(old.lightness), f"same {prop} as {side} input"


class CssArgsParser(ArgsParser):
    name = "css"

    def _parse_args(self) -> None:
        self._parser.add_argument("-l", "--label", type=str, default="color")
        self._parser.add_argument("-c", "--color1", type=str, required=True)
        self._parser.add_argument("-k", "--color2", type=str)
        self._parser.add_argument(
            "-s", "--number-of-shades", type=check_integer_in_range(1, 99), default=19
        )
        self._parser.add_argument(
            "-b", "--include-black-and-white", action="store_true", default=False
        )
        self._parser.add_argument(
            "-i", "--include-input-shades", action="store_true", default=False
        )
        self._parser.add_argument(
            "-d", "--dynamic-range", type=check_integer_in_range(0, 100), default=0
        )

    def _run_command(self, args: Namespace) -> None:
        gen_cls = LinesGeneratorTwoColors if args.color2 else LinesGeneratorOneColor
        print_lines(gen_cls(args).lines())
