# MadMAC [![Build Status](https://travis-ci.com/laminko/madmac.svg?branch=master)](https://travis-ci.com/laminko/madmac)

MAC address generator library for testers.

## Content

- [Installation](#installation)
- [Usage](#usage)
  - [Command](#as-a-command)
  - [Module](#as-a-module)

### Installation

Using `pip`:

> `pip install madmac`

Using source:

```bash
$ git clone https://github.com/laminko/madmac.git
$ cd madmac
$ python setup.py install
```

### Usage

#### As a command

Can be used `madmac` as command. The following will generate random MAC address.

```bash
madmac
```

To see help, enter `madmac --help`.

```bash
madmac --help
usage: madmac [-h] [-o OUI] [-r START] [-s STOP] [-t TOTAL] [-d DELIMITER]
              [-c CASE]

MAC address generator library for testers.

optional arguments:
  -h, --help            show this help message and exit
  -o OUI, --oui OUI     6-digit organizationally unique identifier
  -r START, --start START
                        NIC specific start address
  -s STOP, --stop STOP  NIC specific end address
  -t TOTAL, --total TOTAL
                        Number of MACs to generate
  -d DELIMITER, --delimiter DELIMITER
                        Delimiter for MAC address
  -c CASE, --case CASE  Use lower or upper
```

> **NOTE**: `madmac` is not a binary file. You need to install python 3.5 to execute the command.

#### As a module

Import `MacGenerator` class from `madmac` module. And create an object using `MacGenerator` and call its member `generate()` function. `generate()` function will return python generator object.

The following code will generate single MAC address using default values.

```python
from madmac import MacGenerator

macg = MacGenerator()
macs = macg.generate()  # generator object which contains one item
from pprint import pprint
pprint(list(macs))
```

Default values are as follows:

```python
# 'oui':  None,
# 'start': None,
# 'stop': None,
# 'total': 1,
# 'delimiter': ':',
# 'case': 'lower'
```

One can provide `oui`:

```python
from madmac import MacGenerator

macg = MacGenerator(oui='F0-9F-C2')
list(macg.generate())
```

Also specify `start` address and `end` address if they are known:

```python
from madmac import MacGenerator

start = '00-B0-A0'
stop = '00-B0-DF'
macg = MacGenerator(start=start, stop=stop)
```

> **NOTE**: Above snippet describes to use random `oui`, but to use certain range from `start` and `stop` values. It will ignore `total` parameter. Delimiter and Case will be default values.

Sometimes, we might want to generate certain amount of MAC addresses:

```python
from madmac import MacGenerator

macg = MacGenerator(total=100)
```
