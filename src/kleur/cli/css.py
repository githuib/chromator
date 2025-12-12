from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from kleur import Color, Colored
from kleur.interpol import LinearMapping, mapped

from .utils import ArgsParser, check_integer_in_range, print_lines

if TYPE_CHECKING:
    from argparse import Namespace
    from collections.abc import Iterator


def _colored(s: str, color: Color, *, flipped: bool = False) -> str:
    c, k = color, color.contrasting_shade
    return str(Colored(s, *((c, k) if flipped else (k, c))))


def _css_color_comment(color: Color, *, flipped: bool = False) -> str:
    return _colored(f"#{color.as_hex} --> {color}", color, flipped=flipped)


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

        colors: dict[int, tuple[Color, str]] = {}
        for color, input_indication in self._colors():
            n = round(color.lightness * 100)
            if n not in colors:
                colors[n] = color, input_indication

        generated = sorted(colors.items())
        n_max, _ = generated[-1]
        n_digits = len(str(n_max))
        for n, (color, input_indication) in generated:
            has_ind = input_indication != ""
            i = f" <-- {input_indication}" if has_ind else ""
            css_var = f"--{self._label}-{str(n).zfill(n_digits)}: #{color.as_hex};"
            yield _colored(f"{css_var} /* --> {color}{i} */", color, flipped=has_ind)


class LinesGeneratorOneColor(LinesGenerator):
    def __init__(self, args: Namespace) -> None:
        super().__init__(args)
        self._input = Color.from_hex(args.color1)

    def _comment_lines(self) -> Iterator[str]:
        yield f"Based on: {_css_color_comment(self._input)}"

    def _colors(self) -> Iterator[tuple[Color, str]]:
        """Generate shades of a color."""
        if self._include_input:
            yield self._input, "input"
        for s in self._shades:
            yield self._input.shade(s), ""


def normalize_color(c1: Color, c2: Color) -> Color:
    return c1 if round(c1.saturation, 2) else Color(c2.hue, c1.saturation, c1.lightness)


class LinesGeneratorTwoColors(LinesGenerator):
    def __init__(self, args: Namespace) -> None:
        super().__init__(args)
        self._dynamic_range = args.dynamic_range / 100
        c1, c2 = sorted(Color.from_hex(h) for h in (args.color1, args.color2))
        c1 = normalize_color(c1, c2)
        c2 = normalize_color(c2, c1)
        self._dark_input, self._bright_input = c1, c2

    def _comment_lines(self) -> Iterator[str]:
        yield "Based on:"
        yield f"- Darkest:   {_css_color_comment(self._dark_input)}"
        yield f"- Brightest: {_css_color_comment(self._bright_input)}"

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
        old_dark_shade = self._dark_input.lightness
        new_dark_shade = mapped(self._dynamic_range, (old_dark_shade, 0))
        new_dark = self._dark_input.shade(new_dark_shade)

        old_bright_shade = self._bright_input.lightness
        new_bright_shade = mapped(self._dynamic_range, (old_bright_shade, 1))
        new_bright = self._bright_input.shade(new_bright_shade)

        shade_mapping = LinearMapping(new_dark_shade, new_bright_shade)

        def blend(lightness: float) -> Color:
            return new_dark.blend(new_bright, shade_mapping.position_of(lightness))

        if self._include_input:
            input_indication = "same {} as {} input"
            yield blend(old_dark_shade), input_indication.format("shade", "darkest")
            yield blend(old_bright_shade), input_indication.format("shade", "brightest")
            if self._dynamic_range:
                yield new_dark, input_indication.format("hue", "darkest")
                yield new_bright, input_indication.format("hue", "brightest")

        for s in self._shades:
            yield blend(s), ""


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
