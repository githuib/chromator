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

#### Shades as CSS variables, based on one input color:

```commandline
$ kleur css -l salads -c 5a1ad5 -n 9
/*
Based on:
#5a1ad5 --> Color(hue=271.73°, saturation=93.85%, lightness=33.39%)
*/
--salads-10: #210558; /* --> Color(hue=271.73°, saturation=93.85%, lightness=10.00%) */
--salads-20: #380d8b; /* --> Color(hue=271.73°, saturation=93.85%, lightness=20.00%) */
--salads-30: #5117c2; /* --> Color(hue=271.73°, saturation=93.85%, lightness=30.00%) */
--salads-40: #6a2bf2; /* --> Color(hue=271.73°, saturation=93.85%, lightness=40.00%) */
--salads-50: #8059f6; /* --> Color(hue=271.73°, saturation=93.85%, lightness=50.00%) */
--salads-60: #977df8; /* --> Color(hue=271.73°, saturation=93.85%, lightness=60.00%) */
--salads-70: #af9ffa; /* --> Color(hue=271.73°, saturation=93.85%, lightness=70.00%) */
--salads-80: #c9bffc; /* --> Color(hue=271.73°, saturation=93.85%, lightness=80.00%) */
--salads-90: #e4dffd; /* --> Color(hue=271.73°, saturation=93.85%, lightness=90.00%) */
```

#### Shades as CSS variables, based on one input color (with input markers):

```commandline
$ kleur css -l salads -c 5a1ad5 -n 9
/*
Based on:
#5a1ad5 --> Color(hue=271.73°, saturation=93.85%, lightness=33.39%)
*/
--salads-10: #210558; /* --> Color(hue=271.73°, saturation=93.85%, lightness=10.00%) */
--salads-20: #380d8b; /* --> Color(hue=271.73°, saturation=93.85%, lightness=20.00%) */
--salads-30: #5117c2; /* --> Color(hue=271.73°, saturation=93.85%, lightness=30.00%) */
--salads-33: #5a1ad5; /* --> Color(hue=271.73°, saturation=93.85%, lightness=33.39%) <-- input */
--salads-40: #6a2bf2; /* --> Color(hue=271.73°, saturation=93.85%, lightness=40.00%) */
--salads-50: #8059f6; /* --> Color(hue=271.73°, saturation=93.85%, lightness=50.00%) */
--salads-60: #977df8; /* --> Color(hue=271.73°, saturation=93.85%, lightness=60.00%) */
--salads-70: #af9ffa; /* --> Color(hue=271.73°, saturation=93.85%, lightness=70.00%) */
--salads-80: #c9bffc; /* --> Color(hue=271.73°, saturation=93.85%, lightness=80.00%) */
--salads-90: #e4dffd; /* --> Color(hue=271.73°, saturation=93.85%, lightness=90.00%) */
```

#### Shades as CSS variables, based on two input colors:

```commandline
$ kleur css -l beatle-salads -c bea71e -k 5a1ad5 -n 9 -d 50
/*
Based on:
- Darkest:   #5a1ad5 --> Color(hue=271.73°, saturation=93.85%, lightness=33.39%)
- Brightest: #bea71e --> Color(hue=73.04°, saturation=96.08%, lightness=68.52%)
*/
--beatle-salads-10: #031b3d; /* --> Color(hue=255.75°, saturation=93.63%, lightness=10.00%) */
--beatle-salads-20: #480b79; /* --> Color(hue=279.63°, saturation=93.96%, lightness=20.00%) */
--beatle-salads-30: #7c1082; /* --> Color(hue=303.50°, saturation=94.29%, lightness=30.00%) */
--beatle-salads-40: #ad1589; /* --> Color(hue=327.37°, saturation=94.62%, lightness=40.00%) */
--beatle-salads-50: #e2197e; /* --> Color(hue=351.25°, saturation=94.95%, lightness=50.00%) */
--beatle-salads-60: #fb5847; /* --> Color(hue=15.12°, saturation=95.28%, lightness=60.00%) */
--beatle-salads-70: #f59421; /* --> Color(hue=39.00°, saturation=95.61%, lightness=70.00%) */
--beatle-salads-80: #f1c026; /* --> Color(hue=62.87°, saturation=95.94%, lightness=80.00%) */
--beatle-salads-90: #e8ea2b; /* --> Color(hue=86.74°, saturation=96.27%, lightness=90.00%) */
```

#### Shades as CSS variables, based on two input colors (with input markers):

```commandline
$ kleur css -l beatle-salads -c bea71e -k 5a1ad5 -n 9 -d 50 -i
/*
Based on:
- Darkest:   #5a1ad5 --> Color(hue=271.73°, saturation=93.85%, lightness=33.39%)
- Brightest: #bea71e --> Color(hue=73.04°, saturation=96.08%, lightness=68.52%)
*/
--beatle-salads-10: #031b3d; /* --> Color(hue=255.75°, saturation=93.63%, lightness=10.00%) */
--beatle-salads-17: #300a7a; /* --> Color(hue=271.73°, saturation=93.85%, lightness=16.69%) <-- same hue as darkest input */
--beatle-salads-20: #480b79; /* --> Color(hue=279.63°, saturation=93.96%, lightness=20.00%) */
--beatle-salads-30: #7c1082; /* --> Color(hue=303.50°, saturation=94.29%, lightness=30.00%) */
--beatle-salads-33: #8c1286; /* --> Color(hue=311.58°, saturation=94.40%, lightness=33.39%) <-- same shade as darkest input */
--beatle-salads-40: #ad1589; /* --> Color(hue=327.37°, saturation=94.62%, lightness=40.00%) */
--beatle-salads-50: #e2197e; /* --> Color(hue=351.25°, saturation=94.95%, lightness=50.00%) */
--beatle-salads-60: #fb5847; /* --> Color(hue=15.12°, saturation=95.28%, lightness=60.00%) */
--beatle-salads-69: #f68d21; /* --> Color(hue=35.46°, saturation=95.56%, lightness=68.52%) <-- same shade as brightest input */
--beatle-salads-70: #f59421; /* --> Color(hue=39.00°, saturation=95.61%, lightness=70.00%) */
--beatle-salads-80: #f1c026; /* --> Color(hue=62.87°, saturation=95.94%, lightness=80.00%) */
--beatle-salads-84: #efd228; /* --> Color(hue=73.04°, saturation=96.08%, lightness=84.26%) <-- same hue as brightest input */
--beatle-salads-90: #e8ea2b; /* --> Color(hue=86.74°, saturation=96.27%, lightness=90.00%) */
```

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
 212121  3b3b3b  585858  777777  979797  b9b9b9  dbdbdb      grey
 12.50%  25.00%  37.50%  50.00%  62.50%  75.00%  87.50%
 301b1b  543232  7b4c4c  a36767  ba8c8c  ceb2b2  e5d9d9  012 red
 281e1b  473832  69544b  8c7166  b29082  cfb3a8  e5d9d5  033 orange
 24201e  403a37  5f5752  80756f  a2958d  c5b6ae  e0dad7  042 brown
 23201b  3f3b32  5d584b  7d7666  9f9782  c2b89f  e6dbbf  069 yellow
 1f211a  393d32  555a4b  737a66  929a82  b3bd9f  d4e0bd  101 poison
 1b231a  323f32  4b5d4b  667d66  829f81  9fc29f  bee6bd  127 green
 1b2222  333d3d  4d5b5b  687b7a  859c9b  a3bebd  c1e2e1  190 ocean
 1c2128  353c47  4f5969  6b788d  8898b2  afb9cb  d7dce4  248 blue
 1f1e33  393859  56547e  757399  9594b2  b8b7cb  dbdae4  267 indigo
 241d2e  413751  615276  807099  9e92b2  bdb5cb  dedae4  281 purple
 2b1c25  4c3443  6f4f63  956a85  b58ba5  ccb1c1  e5d8df  329 pink
 12.50%  25.00%  37.50%  50.00%  62.50%  75.00%  87.50%
 3b1414  652828  923d3d  c35354  d57f80  e0acac  eed6d6  012 red
 2e1c14  503527  764f3c  9d6b53  c7896a  e1ad97  eed7ce  033 orange
 261f1b  443932  65554b  887366  ac9282  cfb3a2  e5d9d2  042 brown
 252014  423b27  62583c  837652  a69669  cbb782  efda9f  069 yellow
 1e2214  373e27  525c3c  6f7c52  8e9d69  adc081  cee49a  101 poison
 142413  274127  3d613c  538252  6aa569  83c981  9cef9a  127 green
 152323  293f3f  3f5e5d  567e7d  6ea09f  87c3c2  a2e8e6  190 ocean
 17212f  2c3c53  435a79  5b79a2  7599cc  a5badd  d2dced  248 blue
 1d1b46  363376  524ea2  726fba  9391cc  b6b5dd  dadaed  267 indigo
 29193b  482f66  6a4893  8b66b9  a68bcc  c2b1dd  e0d8ed  281 purple
 34162a  5a2b4a  83426d  af5a92  cf7cb2  dea9c9  eed4e3  329 pink
 12.50%  25.00%  37.50%  50.00%  62.50%  75.00%  87.50%
 440b0c  731a1a  a5292a  db3a3b  ec7272  f0a5a5  f7d3d3  012 red
 331a0b  583219  804b29  ab6639  d8824b  f1a884  f7d4c7  033 orange
 291e17  48382d  6a5444  8f715d  b49076  d9b196  ead8ce  042 brown
 26200b  453b19  655729  887639  ac964a  d2b75c  f8d978  069 yellow
 1d230b  353f19  505e28  6c7e39  89a04a  a8c35c  c8e86e  101 poison
 0c260b  1a4419  2a6428  3b8738  4daa49  5fd05b  72f76d  127 green
 0c2424  1b4140  2c605f  3d8280  4fa4a3  62c9c7  76eeec  190 ocean
 0e2137  1f3d5e  305a89  437ab6  579be5  98bbee  cddcf6  248 blue
 19145b  302898  4b43cb  6e69db  918ee5  b5b3ee  dad9f6  267 indigo
 2e1149  51237c  7637b2  9757db  ae83e5  c7adee  e2d6f6  281 purple
 3c0e2e  671e51  962f77  c7419f  e869bf  efa0d2  f7d1e7  329 pink
 12.50%  25.00%  37.50%  50.00%  62.50%  75.00%  87.50%
 4b0001  7e0002  b50004  ef0007  ff6263  ff9e9f  ffd0d0  012 red
 371900  5f2f00  894700  b76000  e67b00  ffa26d  ffd2c0  033 orange
 2b1e14  4c3727  6f523c  956f52  bc8e6a  e2ae88  eed7c9  042 brown
 282000  473a00  695700  8c7500  b29500  d8b600  ffd935  069 yellow
 1b2400  334000  4d5f00  688000  85a200  a3c600  c2eb00  101 poison
 012700  044600  096700  108a00  17af00  1ed600  26fe00  127 green
 002525  004342  006362  008583  00a9a6  00cecb  00f4f1  190 ocean
 00223e  003e69  005b98  007bca  009cff  89bcff  c8ddff  248 blue
 100079  2100c6  3e29ff  685fff  8e89ff  b4b1ff  d9d8ff  267 indigo
 350059  5c0095  8500d5  a63bff  b879ff  cda8ff  e5d4ff  281 purple
 440033  740059  a70081  dd00ac  ff4ecb  ff96da  ffcdeb  329 pink
```

#### Preview custom theme

```commandline
$ kleur colors -n 7 -c red=11 green=128 blue=249
 212121  3b3b3b  585858  777777  979797  b9b9b9  dbdbdb      grey
 12.50%  25.00%  37.50%  50.00%  62.50%  75.00%  87.50%
 301b1b  543233  7a4c4d  a36768  ba8c8d  ceb2b3  e5d9d9  011 red
 1a231b  323f32  4b5d4b  667d66  829f82  9fc29f  bde6bd  128 green
 1c2128  353c48  4f596a  6b788e  8998b3  b0b9cb  d7dce4  249 blue
 12.50%  25.00%  37.50%  50.00%  62.50%  75.00%  87.50%
 3b1415  65282a  923d3f  c25457  d57f81  e0acad  eed6d6  011 red
 132414  274227  3c613c  528252  69a56a  81c982  9aef9b  128 green
 172130  2c3c54  43597a  5b78a3  7699cc  a6badd  d3dced  249 blue
 12.50%  25.00%  37.50%  50.00%  62.50%  75.00%  87.50%
 430b0e  721a1e  a52a2f  da3a41  ec7275  f0a5a7  f7d3d4  011 red
 0b260b  194419  286429  38873a  49ab4b  5bd05d  6ef770  128 green
 0f2137  1f3d5f  315a8a  4479b8  5b9ae6  9abaee  cedcf6  249 blue
 12.50%  25.00%  37.50%  50.00%  62.50%  75.00%  87.50%
 4a0004  7d000b  b40014  ef001f  ff6267  ff9ea0  ffd0d1  011 red
 002701  004602  006804  008b07  00b00b  00d610  00fe16  128 green
 00223f  003d6b  005b9b  007acd  1f9bff  8cbbff  c9dcff  249 blue
 ```

#### Preview custom theme merged with default theme

```commandline
$ kleur colors -n 7 -c red=11 green=128 blue=249 -m
 212121  3b3b3b  585858  777777  979797  b9b9b9  dbdbdb      grey
 12.50%  25.00%  37.50%  50.00%  62.50%  75.00%  87.50%
 301b1b  543233  7a4c4d  a36768  ba8c8d  ceb2b3  e5d9d9  011 red
 281e1b  473832  69544b  8c7166  b29082  cfb3a8  e5d9d5  033 orange
 24201e  403a37  5f5752  80756f  a2958d  c5b6ae  e0dad7  042 brown
 23201b  3f3b32  5d584b  7d7666  9f9782  c2b89f  e6dbbf  069 yellow
 1f211a  393d32  555a4b  737a66  929a82  b3bd9f  d4e0bd  101 poison
 1a231b  323f32  4b5d4b  667d66  829f82  9fc29f  bde6bd  128 green
 1b2222  333d3d  4d5b5b  687b7a  859c9b  a3bebd  c1e2e1  190 ocean
 1c2128  353c48  4f596a  6b788e  8998b3  b0b9cb  d7dce4  249 blue
 1f1e33  393859  56547e  757399  9594b2  b8b7cb  dbdae4  267 indigo
 241d2e  413751  615276  807099  9e92b2  bdb5cb  dedae4  281 purple
 2b1c25  4c3443  6f4f63  956a85  b58ba5  ccb1c1  e5d8df  329 pink
 12.50%  25.00%  37.50%  50.00%  62.50%  75.00%  87.50%
 3b1415  65282a  923d3f  c25457  d57f81  e0acad  eed6d6  011 red
 2e1c14  503527  764f3c  9d6b53  c7896a  e1ad97  eed7ce  033 orange
 261f1b  443932  65554b  887366  ac9282  cfb3a2  e5d9d2  042 brown
 252014  423b27  62583c  837652  a69669  cbb782  efda9f  069 yellow
 1e2214  373e27  525c3c  6f7c52  8e9d69  adc081  cee49a  101 poison
 132414  274227  3c613c  528252  69a56a  81c982  9aef9b  128 green
 152323  293f3f  3f5e5d  567e7d  6ea09f  87c3c2  a2e8e6  190 ocean
 172130  2c3c54  43597a  5b78a3  7699cc  a6badd  d3dced  249 blue
 1d1b46  363376  524ea2  726fba  9391cc  b6b5dd  dadaed  267 indigo
 29193b  482f66  6a4893  8b66b9  a68bcc  c2b1dd  e0d8ed  281 purple
 34162a  5a2b4a  83426d  af5a92  cf7cb2  dea9c9  eed4e3  329 pink
 12.50%  25.00%  37.50%  50.00%  62.50%  75.00%  87.50%
 430b0e  721a1e  a52a2f  da3a41  ec7275  f0a5a7  f7d3d4  011 red
 331a0b  583219  804b29  ab6639  d8824b  f1a884  f7d4c7  033 orange
 291e17  48382d  6a5444  8f715d  b49076  d9b196  ead8ce  042 brown
 26200b  453b19  655729  887639  ac964a  d2b75c  f8d978  069 yellow
 1d230b  353f19  505e28  6c7e39  89a04a  a8c35c  c8e86e  101 poison
 0b260b  194419  286429  38873a  49ab4b  5bd05d  6ef770  128 green
 0c2424  1b4140  2c605f  3d8280  4fa4a3  62c9c7  76eeec  190 ocean
 0f2137  1f3d5f  315a8a  4479b8  5b9ae6  9abaee  cedcf6  249 blue
 19145b  302898  4b43cb  6e69db  918ee5  b5b3ee  dad9f6  267 indigo
 2e1149  51237c  7637b2  9757db  ae83e5  c7adee  e2d6f6  281 purple
 3c0e2e  671e51  962f77  c7419f  e869bf  efa0d2  f7d1e7  329 pink
 12.50%  25.00%  37.50%  50.00%  62.50%  75.00%  87.50%
 4a0004  7d000b  b40014  ef001f  ff6267  ff9ea0  ffd0d1  011 red
 371900  5f2f00  894700  b76000  e67b00  ffa26d  ffd2c0  033 orange
 2b1e14  4c3727  6f523c  956f52  bc8e6a  e2ae88  eed7c9  042 brown
 282000  473a00  695700  8c7500  b29500  d8b600  ffd935  069 yellow
 1b2400  334000  4d5f00  688000  85a200  a3c600  c2eb00  101 poison
 002701  004602  006804  008b07  00b00b  00d610  00fe16  128 green
 002525  004342  006362  008583  00a9a6  00cecb  00f4f1  190 ocean
 00223f  003d6b  005b9b  007acd  1f9bff  8cbbff  c9dcff  249 blue
 100079  2100c6  3e29ff  685fff  8e89ff  b4b1ff  d9d8ff  267 indigo
 350059  5c0095  8500d5  a63bff  b879ff  cda8ff  e5d4ff  281 purple
 440033  740059  a70081  dd00ac  ff4ecb  ff96da  ffcdeb  329 pink
 ```
