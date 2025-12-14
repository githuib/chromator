from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from math import log10
from typing import TYPE_CHECKING

from kleur import Color, Colored
from kleur.interpol import LinearMapping, mapped

from .utils import ArgsParser, check_integer_in_range, print_lines

if TYPE_CHECKING:
    from argparse import Namespace
    from collections.abc import Callable, Iterator

    from kleur.color import ColorProp


@dataclass(frozen=True)
class Indicator:
    side: str = ""
    props: set[ColorProp] = field(default_factory=set)


def _colored(color: Color) -> Callable[[str], str]:
    def wrapped(s: str) -> str:
        return Colored(s, color.contrasting_shade, color)

    return wrapped


def _colored_props(color: Color, indicator: set[ColorProp]) -> Iterator[str]:
    h_str, s_str, l_str = color.prop_strings.values()
    i_hue, i_sat, i_li = [p in indicator for p in color.prop_strings]

    c_hue = Color(color.hue, lightness=0.5)
    yield _colored(c_hue)(h_str) if i_hue else h_str

    c_sat = c_hue.saturated(color.saturation)
    yield _colored(c_sat)(s_str) if i_sat else s_str

    c_li = c_sat.shade(color.lightness)
    yield _colored(c_li)(l_str) if i_li else l_str


class LinesGenerator(ABC):
    _input_colors: dict[str, Color]

    def __init__(self, args: Namespace) -> None:
        self._include_input = args.include_input_shades
        self._include_bw = args.include_black_and_white
        self._label = args.label
        steps = args.number_of_shades + 1
        shades_range = (0, steps + 1) if self._include_bw else (1, steps)
        self._shades = [s / steps for s in range(*shades_range)]
        self._generated_shades: set[int] = set()

    def _comment_lines(self) -> Iterator[str]:
        yield "Based on:"
        for side, color in self._input_colors.items():
            side_str = f"{side.capitalize()}:"
            yield f"- {side_str:<10} {_colored(color)(f'#{color.as_hex}')} --> {color}"

    @abstractmethod
    def _colors(self) -> Iterator[tuple[Color, Indicator]]: ...

    def lines(self) -> Iterator[str]:
        yield "/*"
        yield from self._comment_lines()
        yield "*/"

        colors = {round(c.lightness * 100): (c, i) for c, i in self._colors()}
        n_digits = int(log10(max(colors.keys()))) + 1
        for s, (c, i) in sorted(colors.items()):
            cf = _colored(c)

            css_var = cf(f"--{self._label}-{str(s).zfill(n_digits)}: #{c.as_hex};")

            comment = f" --> HSLuv({', '.join(_colored_props(c, i.props))})"
            if i.side:
                p_str = {1: next(iter(i.props)), 2: " & ".join(i.props), 3: "color"}
                side = _colored(self._input_colors[i.side])(f"{i.side} input")
                comment += f" <-- same {p_str[len(i.props)]} as {side}"

            yield f"{css_var} /* {comment} */"


class LinesGeneratorOneColor(LinesGenerator):
    def __init__(self, args: Namespace) -> None:
        super().__init__(args)
        self._input_color = Color.from_hex(args.color1)
        self._input_colors = {"input": self._input_color}

    def _colors(self) -> Iterator[tuple[Color, Indicator]]:
        """Generate shades of a color."""
        for s in self._shades:
            yield self._input_color.shade(s), Indicator()

        if self._include_input:
            yield (
                self._input_color,
                Indicator("input", {"hue", "saturation", "lightness"}),
            )


def normalize_color(c1: Color, c2: Color) -> Color:
    return c1 if round(c1.saturation, 2) else c1.shifted(c2.hue)


class LinesGeneratorTwoColors(LinesGenerator):
    def __init__(self, args: Namespace) -> None:
        super().__init__(args)
        self._dynamic_range = args.dynamic_range / 100
        c1, c2 = Color.from_hex(args.color1), Color.from_hex(args.color2)
        c1 = normalize_color(c1, c2)
        c2 = normalize_color(c2, c1)
        self._dark, self._bright = sorted((c1, c2))
        self._input_colors = {"darkest": self._dark, "brightest": self._bright}

    def _colors(self) -> Iterator[tuple[Color, Indicator]]:
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
            for i, c in enumerate(self._input_colors.values())
        ]
        shade_mapping = LinearMapping(dark.lightness, bright.lightness)

        def blend(lightness: float) -> Color:
            return dark.blend(bright, shade_mapping.position_of(lightness))

        for s in self._shades:
            yield blend(s), Indicator()

        if self._include_input:
            sides = "darkest", "brightest"
            for side, old, new in zip(
                sides, self._input_colors.values(), mapping_colors, strict=True
            ):
                if old.as_hex == new.as_hex:
                    yield new, Indicator(side, {"hue", "saturation", "lightness"})
                else:
                    yield blend(old.lightness), Indicator(side, {"lightness"})
                    yield new, Indicator(side, {"hue", "saturation"})


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
