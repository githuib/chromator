# Kleur: [HSLuv](https://www.hsluv.org/) based color utils & theme generators

[![Poetry](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/githuib/kleur/master/assets/logo.json)](https://pypi.org/project/kleur)
[![PyPI - Version](https://img.shields.io/pypi/v/kleur)](https://pypi.org/project/kleur/#history)
[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/kleur)](https://pypi.org/project/kleur)

## Installation

```commandline
pip install kleur
```

## Usage

### Generate shades based one 1 or 2 colors (as CSS variables)

#### General help

```commandline
usage: kleur css [-h] [-l LABEL] -c COLOR1 [-k COLOR2] [-n AMOUNT] [-b] [-i] [-d DYNAMIC_RANGE]

options:
  -h, --help            show this help message and exit
  -l, --label LABEL
  -c, --color1 COLOR1
  -k, --color2 COLOR2
  -n, --amount AMOUNT
  -b, --include-black-and-white
  -i, --include-input-shades
  -d, --dynamic-range DYNAMIC_RANGE
```

#### Shades as CSS variables, based on one input color

```commandline
$ kleur css doodle -c d00d1e -n 9
```
![alt text](https://github.com/githuib/kleur/raw/master/assets/screenshots/css/single.png "kleur css doodle -c d00d1e -n 9 -i")

#### Shades as CSS variables, based on one input color (with input markers)

```commandline
$ kleur css doodle -c d00d1e -n 9 -i
```
![alt text](https://github.com/githuib/kleur/raw/master/assets/screenshots/css/single_input.png "kleur css doodle -c d00d1e -n 9 -i")

#### Shades as CSS variables, based on two input colors

```commandline
$ kleur css -l beatle-salads -c bea71e -k 5a1ad5 -n 9 -d 66
```
![alt text](https://github.com/githuib/kleur/raw/master/assets/screenshots/css/double.png "kleur css -l beatle-salads -c bea71e -k 5a1ad5 -n 9 -d 66")

#### Shades as CSS variables, based on two input colors (with input markers)

```commandline
$ kleur css -l beatle-salads -c bea71e -k 5a1ad5 -n 9 -d 0 -i
```
![alt text](https://github.com/githuib/kleur/raw/master/assets/screenshots/css/double_0.png "kleur css -l beatle-salads -c bea71e -k 5a1ad5 -n 9 -d 0 -i")

```commandline
$ kleur css -l beatle-salads -c bea71e -k 5a1ad5 -n 9 -d 50 -i
```
![alt text](https://github.com/githuib/kleur/raw/master/assets/screenshots/css/double_50.png "kleur css -l beatle-salads -c bea71e -k 5a1ad5 -n 9 -d 50 -i")

```commandline
$ kleur css -l beatle-salads -c bea71e -k 5a1ad5 -n 9 -d 100 -i
```
![alt text](https://github.com/githuib/kleur/raw/master/assets/screenshots/css/double_100.png "kleur css -l beatle-salads -c bea71e -k 5a1ad5 -n 9 -d 100 -i")

### Preview a color theme

#### General help

```commandline
$ kleur colors -h
usage: kleur colors [-h] [-c NAME=HUE (1-360) [NAME=HUE (1-360) ...]] [-m] [-a] [-n NUM_SHADES]

options:
  -h, --help            show this help message and exit
  -c, --color-hues NAME=HUE (1-360) [NAME=HUE (1-360) ...]
  -m, --merge-with-default-theme
  -a, --alt-default-theme
  -n, --num-shades NUM_SHADES
```

#### Preview default theme

```commandline
$ uv run kleur colors -n 7
```
![alt text](https://github.com/githuib/kleur/raw/master/assets/screenshots/colors/default.png "kleur colors -n 7")

#### Preview custom theme

```commandline
$ kleur colors -n 7 -c green=133 blue=257 tomato=20
 ```
![alt text](https://github.com/githuib/kleur/raw/master/assets/screenshots/colors/custom.png "kleur colors -n 7 -c green=133 blue=257 tomato=20")

#### Preview custom theme merged with default theme

```commandline
$ kleur colors -n 7 -c green=133 blue=257 tomato=20 -m
 ```
![alt text](https://github.com/githuib/kleur/raw/master/assets/screenshots/colors/merged.png "kleur colors -n 7 -c green=133 blue=257 tomato=20 -m")
