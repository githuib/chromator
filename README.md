# Chromator: Color shades generator

[![Poetry](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/githuib/chromator/master/assets/logo.json)](https://pypi.org/project/chromator)
[![PyPI - Version](https://img.shields.io/pypi/v/chromator)](https://pypi.org/project/chromator/#history)
[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/chromator)](https://pypi.org/project/chromator)

## Installation

```commandline
pip install chromator
```

## Usage

### General help

```commandline
$ chromator -h
usage: chromator [-h] [-c COLOR1] [-k COLOR2] [-n AMOUNT] [-i] [-d DYNAMIC_RANGE] label

positional arguments:
  label

options:
  -h, --help            show this help message and exit
  -c, --color1 COLOR1
  -k, --color2 COLOR2
  -n, --amount AMOUNT
  -i, --inclusive
  -d, --dynamic-range DYNAMIC_RANGE
```

### Shades as CSS variables, based on one input color:

```commandline
$ chromator bad-ass -c bada55 -n 9
/*
Based on:
#bada55 --> Color(hue=100.61°, saturation=82.87%, lightness=82.51%)
*/
--bad-ass-10: #181e06; /* --> Color(hue=100.61°, saturation=82.87%, lightness=10.00%) */
--bad-ass-20: #2b340e; /* --> Color(hue=100.61°, saturation=82.87%, lightness=20.00%) */
--bad-ass-30: #3f4c18; /* --> Color(hue=100.61°, saturation=82.87%, lightness=30.00%) */
--bad-ass-40: #556523; /* --> Color(hue=100.61°, saturation=82.87%, lightness=40.00%) */
--bad-ass-50: #6b7f2e; /* --> Color(hue=100.61°, saturation=82.87%, lightness=50.00%) */
--bad-ass-60: #839a3a; /* --> Color(hue=100.61°, saturation=82.87%, lightness=60.00%) */
--bad-ass-70: #9bb646; /* --> Color(hue=100.61°, saturation=82.87%, lightness=70.00%) */
--bad-ass-80: #b4d352; /* --> Color(hue=100.61°, saturation=82.87%, lightness=80.00%) */
--bad-ass-90: #cdf05f; /* --> Color(hue=100.61°, saturation=82.87%, lightness=90.00%) */
```

### Shades as CSS variables, based on two input colors:

```commandline
$ chromator worse-ass -c bada55 -k b000b5 -n 9 -d 50
/*
Based on:
- Darkest:   #b000b5 --> Color(hue=305.50°, saturation=100.00%, lightness=42.10%)
- Brightest: #bada55 --> Color(hue=100.61°, saturation=82.87%, lightness=82.51%)
*/
--worse-ass-10: #2e004e; /* --> Color(hue=281.09°, saturation=100.00%, lightness=10.00%) */
--worse-ass-20: #5a005f; /* --> Color(hue=303.18°, saturation=100.00%, lightness=20.00%) */
--worse-ass-30: #86066c; /* --> Color(hue=325.27°, saturation=97.82%, lightness=30.00%) */
--worse-ass-40: #b5116b; /* --> Color(hue=347.37°, saturation=95.38%, lightness=40.00%) */
--worse-ass-50: #e91d39; /* --> Color(hue=9.46°, saturation=92.94%, lightness=50.00%) */
--worse-ass-60: #da762a; /* --> Color(hue=31.56°, saturation=90.50%, lightness=60.00%) */
--worse-ass-70: #daa13a; /* --> Color(hue=53.65°, saturation=88.06%, lightness=70.00%) */
--worse-ass-80: #dbc84b; /* --> Color(hue=75.75°, saturation=85.62%, lightness=80.00%) */
--worse-ass-90: #d3ef5e; /* --> Color(hue=97.84°, saturation=83.18%, lightness=90.00%) */
```
