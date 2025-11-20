# Chromator: Color shades generator

[![Poetry](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/githuib/chromator/master/assets/logo.json)](https://pypi.org/project/chromator)
[![PyPI - Version](https://img.shields.io/pypi/v/chromator)](https://pypi.org/project/chromator/#history)
[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/chromator)](https://pypi.org/project/chromator)

## Installation

```commandline
pip install chromator
```

## Usage

### Generate shades based one 1 or 2 colors (as CSS variables)

#### General help

```commandline
$ chromator css -h
usage: chromator css [-h] [-l LABEL] [-c COLOR1] [-k COLOR2] [-n AMOUNT] [-i]
                     [-d DYNAMIC_RANGE]

options:
  -h, --help            show this help message and exit
  -l, --label LABEL
  -c, --color1 COLOR1
  -k, --color2 COLOR2
  -n, --amount AMOUNT
  -i, --inclusive
  -d, --dynamic-range DYNAMIC_RANGE
```

#### Shades as CSS variables, based on one input color:

```commandline
$ chromator css -l bad-ass -c bada55 -n 9
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

#### Shades as CSS variables, based on two input colors:

```commandline
$ chromator css -l worse-ass -c bada55 -k b000b5 -n 9 -d 50
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

### Preview a color theme

#### General help

```commandline
$ chromator colors -h
usage: chromator colors [-h] [--red RED] [--orange ORANGE] [--yellow YELLOW]
                        [--poison POISON] [--green GREEN] [--ocean OCEAN]
                        [--blue BLUE] [--indigo INDIGO] [--purple PURPLE]
                        [--pink PINK]

options:
  -h, --help            show this help message and exit
  --red RED
  --orange ORANGE
  --yellow YELLOW
  --poison POISON
  --green GREEN
  --ocean OCEAN
  --blue BLUE
  --indigo INDIGO
  --purple PURPLE
  --pink PINK
```

#### Preview default theme

```commandline
$ chromator colors
 111111  1b1b1b  262626  303030  3b3b3b  474747  525252  5e5e5e  6a6a6a  777777  848484  919191  9e9e9e  ababab  b9b9b9  c6c6c6  d4d4d4  e2e2e2  f1f1f1      grey
   5%     10%     15%     20%     25%     30%     35%     40%     45%     50%     55%     60%     65%     70%     75%     80%     85%     90%     95%
 1b0d0e  291617  371f20  45292a  533234  623c3e  724748  825153  925c5e  a36769  b07476  b68486  bd9395  c5a3a4  ceb2b3  d7c2c2  e0d1d1  eae0e0  f4f0f0  010 red
 16100d  221a16  2e241f  3a2e28  473832  54433c  614e46  6f5a50  7d665b  8b7266  9a7e71  a98a7c  b89788  c7a494  cfb3a7  d7c2ba  e0d1cb  eae1dd  f4f0ee  035 orange
 12110d  1d1c16  27261f  323028  3e3b32  4a473c  565246  625e50  6f6b5b  7c7766  898471  96917c  a49e88  b1ab93  bfb99f  cec7ab  dcd5b7  ebe3c3  f4f1e3  075 yellow
 10110d  1a1c16  24271f  2f3128  393d32  44483c  505446  5b6050  676d5b  737966  808671  8c947c  99a187  a6af93  b3bc9f  c1caab  ced9b7  dce7c3  ebf5d6  100 poison
 0d120d  161d16  1f281f  293328  323e32  3c4a3c  475746  516350  5c705b  677d66  728a71  7d977c  89a587  95b393  a0c19f  add0ab  b9deb7  cbebca  e7f4e6  126 green
 0d1211  171d1c  202726  293231  333d3c  3d4948  475554  526160  5d6e6c  687b79  738886  7f9593  8aa3a0  96b0ae  a2bebc  afccca  bbdbd8  c7e9e6  e3f4f3  184 ocean
 0e1115  181c21  21262d  2a3139  343c45  3f4852  49535f  545f6d  5f6c7b  6a7889  768597  8292a6  8ea0b5  9cadc1  acbacb  bdc7d5  cdd5df  dee3ea  eef1f4  242 blue
 100f1d  1b192c  25233a  2f2d49  3a3858  454368  514e78  5d5a83  69668f  767399  8280a3  8f8ead  9d9bb7  aaa9c1  b8b7cb  c6c5d5  d4d3df  e2e2ea  f0f0f4  268 indigo
 130f1a  1f1928  2a2235  352c43  413751  4d4160  5a4c6f  66577f  74638e  7f7099  8b7da3  978bad  a499b7  b0a7c1  bdb5cb  cac4d5  d7d2df  e4e1ea  f1f0f4  280 purple
 180e14  241820  31212c  3e2a38  4b3444  593f50  67495d  76546b  855f78  946b86  a37695  b083a1  b993ac  c2a2b7  ccb1c3  d6c1ce  e0d0da  eae0e6  f4eff2  325 pink
   5%     10%     15%     20%     25%     30%     35%     40%     45%     50%     55%     60%     65%     70%     75%     80%     85%     90%     95%
 22090a  331012  43181a  532022  64282b  763034  88393d  9b4246  ae4b50  c15459  d06167  d3767a  d7898c  db9a9d  e0acae  e5bdbe  ebcdce  f1dedf  f8efef  010 red
 190e08  271810  342218  412b1f  4f3527  5e402f  6d4b38  7c5641  8b6149  9b6c53  ab785c  bc8465  cd906f  dd9d79  e1ae94  e6beac  ebcec2  f1dfd7  f8efeb  035 orange
 131108  1e1c10  292617  34301f  403b27  4c472f  595338  655f40  726b49  807752  8d845b  9b9165  a99e6e  b7ac78  c5b982  d4c78c  e3d596  f2e3a0  f8f1d5  075 yellow
 0f1208  191d10  232817  2d331f  383e27  424a2f  4d5638  596240  646f49  707c52  7c895b  889664  95a46e  a2b278  aec081  bbce8b  c9dd95  d6eb9f  e6f8b8  100 poison
 091308  111f10  182a17  20351f  284127  314e2f  3a5a37  426740  4b7449  558252  5e8f5b  689d64  72ac6e  7bba77  86c981  90d88b  9ae795  b3f2af  dcf8db  126 green
 091312  111e1d  192927  213432  293f3d  324b49  3a5855  436461  4c716e  567e7b  5f8c88  699995  73a7a3  7db5b1  87c4be  91d2cd  9ce1db  a6f0e9  d4f8f4  184 ocean
 0a1219  121c26  1a2733  233241  2b3d4f  34495d  3d556c  47617b  506d8a  5a7a9a  6487aa  6e94ba  78a2cb  89afd6  9ebcdd  b2c9e3  c6d6ea  d9e3f1  ecf1f8  242 blue
 0f0d29  1a163c  231f4e  2e2961  383274  433c89  4e479d  5a53a7  6761b1  746eba  817cc1  8e8ac9  9c98d0  a9a6d6  b7b5dd  c5c3e3  d3d2ea  e2e1f1  f0f0f8  268 indigo
 160c23  221534  2e1d44  3b2655  483067  553979  62438b  704d9e  7e58b1  8966b9  9475c1  9f84c8  aa93cf  b6a2d6  c1b2dd  cdc1e3  d9d0ea  e6e0f1  f2eff8  280 purple
 1d0a18  2c1325  3b1b31  4a233f  592b4c  69345a  7a3d68  8a4777  9c5086  ad5a95  bf64a5  cc72b2  d285ba  d897c3  dea9cc  e4bad6  eacce0  f1ddea  f8eef4  325 pink
   5%     10%     15%     20%     25%     30%     35%     40%     45%     50%     55%     60%     65%     70%     75%     80%     85%     90%     95%
 280406  3a090c  4c0e13  5f141a  721a21  862028  9a272f  af2d37  c4343f  da3b46  e94a55  eb666d  ec7d82  ee9195  f0a5a8  f3b8ba  f5cacb  f8dcdd  fcedee  010 red
 1c0d04  2b1708  39200e  472913  573319  663d1f  764726  87512c  975c33  a86739  ba7240  cc7e47  de894e  ef9556  f1a87f  f3ba9e  f6ccb9  f8ddd1  fceee9  035 orange
 141104  1f1c08  2a260e  363113  423c19  4e471f  5b5325  685f2c  766b32  837739  918440  9f9146  ad9e4d  bcac55  cbb95c  dac763  e9d56b  f8e372  fcf1c6  075 yellow
 0f1204  181e08  22280d  2c3413  363f19  404b1f  4b5725  56642c  617132  6d7e39  798b3f  859946  91a74d  9db554  aac35c  b6d163  c3e06a  d0ef72  e1fc94  100 poison
 051404  0a2008  102c0d  163713  1c4419  23501f  2a5d25  316b2b  387832  3f8638  46943f  4ea346  55b14d  5dc054  65cf5b  6ddf62  75ee6a  97f990  d2fccf  126 green
 051312  091f1d  0f2a28  153533  1b413f  224e4a  285a57  2f6763  367470  3d827d  44908a  4b9e98  53aca5  5abab3  62c9c1  69d8d0  71e7de  79f6ed  c3fbf6  184 ocean
 05121d  0b1d2c  11283a  173349  1e3e58  254a68  2c5678  336288  3a6f99  427cab  4989bc  5196ce  59a4e0  6fb1eb  8cbdee  a6caf1  bed7f5  d4e4f8  eaf1fb  242 blue
 0e0937  18104e  211865  2b207d  352895  3f30ae  4a39c7  5749cf  6458d5  7167db  7f77df  8d86e4  9a95e7  a8a4eb  b6b3ee  c5c2f1  d3d1f5  e2e0f8  f0f0fb  268 indigo
 19072d  270e41  341554  421c68  50247d  5e2b93  6d33a9  7c3bbf  8b45d5  9558db  9e6adf  a77ce3  b18ce7  bb9deb  c6aeee  d1bef1  dccef5  e7def8  f3effb  280 purple
 23051b  340b2a  441137  551745  661e54  782563  8b2c73  9e3383  b13b93  c542a4  d94ab5  e65bc2  e974c8  ec8bcf  efa0d6  f2b4de  f5c7e5  f8daee  fbedf6  325 pink
   5%     10%     15%     20%     25%     30%     35%     40%     45%     50%     55%     60%     65%     70%     75%     80%     85%     90%     95%
 2d0002  410005  540008  68000d  7d0012  930017  a9001c  bf0021  d70026  ee002c  ff253d  ff525e  ff6f77  ff888d  ff9ea2  ffb3b5  ffc6c8  ffdadb  ffeced  010 red
 1f0c00  2e1500  3d1e00  4d2700  5d3000  6d3900  7e4300  904d00  a15800  b46200  c66d00  d97800  ec8300  ff8e0a  ffa365  ffb68e  ffc9af  ffdbcc  ffede6  035 orange
 141100  201c00  2c2600  383100  443c00  504700  5d5300  6b5f00  786b00  867800  958400  a39100  b29f00  c1ac00  d0ba00  dfc700  eed500  fee300  fff1b6  075 yellow
 0e1300  171e00  212900  2a3400  344000  3e4c00  495900  546500  5f7200  6a8000  758d00  819b00  8da900  99b700  a5c600  b2d400  bee300  cbf200  dcff65  100 poison
 011500  022100  042d00  063900  094600  0d5300  116000  156e00  197c00  1d8a00  219800  25a700  29b600  2dc600  32d500  36e500  3af500  75ff68  c7ffc4  126 green
 001413  00201e  002b29  003734  004340  00504c  005d58  006a65  007871  00857f  00948c  00a29a  00b0a8  00bfb6  00cec4  00ded3  00ede1  00fdf0  b1fff8  184 ocean
 001221  001e31  002840  003350  003f61  004b72  005784  006496  0071a8  007ebb  008bce  0099e2  00a6f6  44b3ff  75bfff  97cbff  b5d8ff  cfe5ff  e8f2ff  242 blue
 0b0049  140067  1c0084  2500a2  2e00c1  3700e1  4106ff  5132ff  604aff  6e5dff  7c6fff  8b80ff  9990ff  a7a0ff  b6b0ff  c4c0ff  d3d0ff  e1dfff  f0efff  268 indigo
 1e0037  2d004f  3b0066  4a007e  5a0097  6a00b1  7b00cb  8c00e6  9c0bff  a23eff  a95aff  b170ff  b984ff  c297ff  cba9ff  d4bbff  dfccff  e9ddff  f4eeff  280 purple
 28001f  3b002e  4d003d  60004c  73005c  87006d  9b007e  b0008f  c600a1  dc00b3  f200c5  ff31d2  ff5ed6  ff7cdb  ff95e0  ffade5  ffc2eb  ffd7f1  ffebf8  325 pink
```

#### Preview custom theme

```commandline
$ chromator colors --red 7 --blue 250
 111111  1b1b1b  262626  303030  3b3b3b  474747  525252  5e5e5e  6a6a6a  777777  848484  919191  9e9e9e  ababab  b9b9b9  c6c6c6  d4d4d4  e2e2e2  f1f1f1      grey
   5%     10%     15%     20%     25%     30%     35%     40%     45%     50%     55%     60%     65%     70%     75%     80%     85%     90%     95%
 1b0d0e  291718  362022  44292b  533335  623d40  71474b  815156  915c61  a1676c  af7479  b68488  bd9397  c5a3a5  cdb2b4  d7c2c3  e0d1d2  eae0e1  f4f0f0  007 red
 16100d  221a16  2e241f  3a2e28  473832  54433c  614e46  6f5a50  7d665b  8b7266  9a7e71  a98a7c  b89788  c7a494  cfb3a7  d7c2ba  e0d1cb  eae1dd  f4f0ee  035 orange
 12110d  1d1c16  27261f  323028  3e3b32  4a473c  565246  625e50  6f6b5b  7c7766  898471  96917c  a49e88  b1ab93  bfb99f  cec7ab  dcd5b7  ebe3c3  f4f1e3  075 yellow
 10110d  1a1c16  24271f  2f3128  393d32  44483c  505446  5b6050  676d5b  737966  808671  8c947c  99a187  a6af93  b3bc9f  c1caab  ced9b7  dce7c3  ebf5d6  100 poison
 0d120d  161d16  1f281f  293328  323e32  3c4a3c  475746  516350  5c705b  677d66  728a71  7d977c  89a587  95b393  a0c19f  add0ab  b9deb7  cbebca  e7f4e6  126 green
 0d1211  171d1c  202726  293231  333d3c  3d4948  475554  526160  5d6e6c  687b79  738886  7f9593  8aa3a0  96b0ae  a2bebc  afccca  bbdbd8  c7e9e6  e3f4f3  184 ocean
 0e1116  181c23  21262f  2b313b  353c48  3f4756  4a5363  555f71  606b80  6b778f  77849e  8391ad  919eb7  a1acc1  b0b9cb  c0c7d5  cfd4df  dfe2ea  eff1f4  250 blue
 100f1d  1b192c  25233a  2f2d49  3a3858  454368  514e78  5d5a83  69668f  767399  8280a3  8f8ead  9d9bb7  aaa9c1  b8b7cb  c6c5d5  d4d3df  e2e2ea  f0f0f4  268 indigo
 130f1a  1f1928  2a2235  352c43  413751  4d4160  5a4c6f  66577f  74638e  7f7099  8b7da3  978bad  a499b7  b0a7c1  bdb5cb  cac4d5  d7d2df  e4e1ea  f1f0f4  280 purple
 180e14  241820  31212c  3e2a38  4b3444  593f50  67495d  76546b  855f78  946b86  a37695  b083a1  b993ac  c2a2b7  ccb1c3  d6c1ce  e0d0da  eae0e6  f4eff2  325 pink
   5%     10%     15%     20%     25%     30%     35%     40%     45%     50%     55%     60%     65%     70%     75%     80%     85%     90%     95%
 22090c  321115  42181d  522026  63282f  753139  873942  9a424c  ac4b56  c05461  cf616d  d3757f  d6888f  db9aa0  e0acb0  e5bdc0  ebcdd0  f1dedf  f8eeef  007 red
 190e08  271810  342218  412b1f  4f3527  5e402f  6d4b38  7c5641  8b6149  9b6c53  ab785c  bc8465  cd906f  dd9d79  e1ae94  e6beac  ebcec2  f1dfd7  f8efeb  035 orange
 131108  1e1c10  292617  34301f  403b27  4c472f  595338  655f40  726b49  807752  8d845b  9b9165  a99e6e  b7ac78  c5b982  d4c78c  e3d596  f2e3a0  f8f1d5  075 yellow
 0f1208  191d10  232817  2d331f  383e27  424a2f  4d5638  596240  646f49  707c52  7c895b  889664  95a46e  a2b278  aec081  bbce8b  c9dd95  d6eb9f  e6f8b8  100 poison
 091308  111f10  182a17  20351f  284127  314e2f  3a5a37  426740  4b7449  558252  5e8f5b  689d64  72ac6e  7bba77  86c981  90d88b  9ae795  b3f2af  dcf8db  126 green
 091312  111e1d  192927  213432  293f3d  324b49  3a5855  436461  4c716e  567e7b  5f8c88  699995  73a7a3  7db5b1  87c4be  91d2cd  9ce1db  a6f0e9  d4f8f4  184 ocean
 0b111b  131c2a  1b2638  243146  2c3c55  354764  3f5374  485f84  526b94  5c78a5  6685b6  7092c7  829fd0  95acd6  a7b9dd  b9c7e3  cad5ea  dce3f1  eef1f8  250 blue
 0f0d29  1a163c  231f4e  2e2961  383274  433c89  4e479d  5a53a7  6761b1  746eba  817cc1  8e8ac9  9c98d0  a9a6d6  b7b5dd  c5c3e3  d3d2ea  e2e1f1  f0f0f8  268 indigo
 160c23  221534  2e1d44  3b2655  483067  553979  62438b  704d9e  7e58b1  8966b9  9475c1  9f84c8  aa93cf  b6a2d6  c1b2dd  cdc1e3  d9d0ea  e6e0f1  f2eff8  280 purple
 1d0a18  2c1325  3b1b31  4a233f  592b4c  69345a  7a3d68  8a4777  9c5086  ad5a95  bf64a5  cc72b2  d285ba  d897c3  dea9cc  e4bad6  eacce0  f1ddea  f8eef4  325 pink
   5%     10%     15%     20%     25%     30%     35%     40%     45%     50%     55%     60%     65%     70%     75%     80%     85%     90%     95%
 270409  3a0910  4c0e18  5e1420  711a28  852130  992739  ad2e41  c3344a  d83b54  e94960  ea6575  ec7c88  ee919a  f0a5ab  f3b7bc  f5cacd  f8dcde  fcedee  007 red
 1c0d04  2b1708  39200e  472913  573319  663d1f  764726  87512c  975c33  a86739  ba7240  cc7e47  de894e  ef9556  f1a87f  f3ba9e  f6ccb9  f8ddd1  fceee9  035 orange
 141104  1f1c08  2a260e  363113  423c19  4e471f  5b5325  685f2c  766b32  837739  918440  9f9146  ad9e4d  bcac55  cbb95c  dac763  e9d56b  f8e372  fcf1c6  075 yellow
 0f1204  181e08  22280d  2c3413  363f19  404b1f  4b5725  56642c  617132  6d7e39  798b3f  859946  91a74d  9db554  aac35c  b6d163  c3e06a  d0ef72  e1fc94  100 poison
 051404  0a2008  102c0d  163713  1c4419  23501f  2a5d25  316b2b  387832  3f8638  46943f  4ea346  55b14d  5dc054  65cf5b  6ddf62  75ee6a  97f990  d2fccf  126 green
 051312  091f1d  0f2a28  153533  1b413f  224e4a  285a57  2f6763  367470  3d827d  44908a  4b9e98  53aca5  5abab3  62c9c1  69d8d0  71e7de  79f6ed  c3fbf6  184 ocean
 061121  0c1c31  122640  183150  1f3c61  264872  2d5483  356095  3c6ca8  4479bb  4c86ce  5493e1  6da0e7  85adeb  9cbaee  b1c7f1  c5d5f5  d9e3f8  ecf1fb  250 blue
 0e0937  18104e  211865  2b207d  352895  3f30ae  4a39c7  5749cf  6458d5  7167db  7f77df  8d86e4  9a95e7  a8a4eb  b6b3ee  c5c2f1  d3d1f5  e2e0f8  f0f0fb  268 indigo
 19072d  270e41  341554  421c68  50247d  5e2b93  6d33a9  7c3bbf  8b45d5  9558db  9e6adf  a77ce3  b18ce7  bb9deb  c6aeee  d1bef1  dccef5  e7def8  f3effb  280 purple
 23051b  340b2a  441137  551745  661e54  782563  8b2c73  9e3383  b13b93  c542a4  d94ab5  e65bc2  e974c8  ec8bcf  efa0d6  f2b4de  f5c7e5  f8daee  fbedf6  325 pink
   5%     10%     15%     20%     25%     30%     35%     40%     45%     50%     55%     60%     65%     70%     75%     80%     85%     90%     95%
 2c0006  40000c  540012  680018  7c001f  920026  a8002d  be0035  d5003c  ed0044  ff2151  ff516a  ff6e80  ff8794  ff9da7  ffb2b9  ffc6cb  ffd9dc  ffecee  007 red
 1f0c00  2e1500  3d1e00  4d2700  5d3000  6d3900  7e4300  904d00  a15800  b46200  c66d00  d97800  ec8300  ff8e0a  ffa365  ffb68e  ffc9af  ffdbcc  ffede6  035 orange
 141100  201c00  2c2600  383100  443c00  504700  5d5300  6b5f00  786b00  867800  958400  a39100  b29f00  c1ac00  d0ba00  dfc700  eed500  fee300  fff1b6  075 yellow
 0e1300  171e00  212900  2a3400  344000  3e4c00  495900  546500  5f7200  6a8000  758d00  819b00  8da900  99b700  a5c600  b2d400  bee300  cbf200  dcff65  100 poison
 011500  022100  042d00  063900  094600  0d5300  116000  156e00  197c00  1d8a00  219800  25a700  29b600  2dc600  32d500  36e500  3af500  75ff68  c7ffc4  126 green
 001413  00201e  002b29  003734  004340  00504c  005d58  006a65  007871  00857f  00948c  00a29a  00b0a8  00bfb6  00cec4  00ded3  00ede1  00fdf0  b1fff8  184 ocean
 001126  001c37  002749  00325a  003d6d  004880  005493  0060a7  006dbc  007ad1  0087e6  0094fc  4ca0ff  71adff  8ebaff  a8c8ff  bfd5ff  d5e3ff  eaf1ff  250 blue
 0b0049  140067  1c0084  2500a2  2e00c1  3700e1  4106ff  5132ff  604aff  6e5dff  7c6fff  8b80ff  9990ff  a7a0ff  b6b0ff  c4c0ff  d3d0ff  e1dfff  f0efff  268 indigo
 1e0037  2d004f  3b0066  4a007e  5a0097  6a00b1  7b00cb  8c00e6  9c0bff  a23eff  a95aff  b170ff  b984ff  c297ff  cba9ff  d4bbff  dfccff  e9ddff  f4eeff  280 purple
 28001f  3b002e  4d003d  60004c  73005c  87006d  9b007e  b0008f  c600a1  dc00b3  f200c5  ff31d2  ff5ed6  ff7cdb  ff95e0  ffade5  ffc2eb  ffd7f1  ffebf8  325 pink
```
