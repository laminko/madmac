# MadMAC [![Build Status](https://travis-ci.com/laminko/madmac.svg?branch=master)](https://travis-ci.com/laminko/madmac)

MAC address generator library for testers.

## Content

- [Install](#installation)
- [Usage](#usage)


### Installation

Using `pip`:

> `pip install madmac`


Using source:

> `git clone https://github.com/laminko/madmac.git`

> `cd madmac`

> `python setup.py install`


### Usage

#### Basic usage

```python
from madmac import MacGenerator

macg = MacGenerator()
macs = macg.generate()  # generator object which contains one item
from pprint import pprint
pprint(list(macs))
```

It will use default values. Default values are as follows:

```python
from madmac import MacGenerator

default_values = {
    'oui':  None,
    'start': None,
    'stop': None,
    'total': 1,
    'delimiter': ':',
    'case': 'lower'
}

macg = MacGenerator(**default_values)
```

#### Custom OUI

```python
from madmac import MacGenerator

macg = MacGenerator(oui='F0-9F-C2')
list(macg.generate())
```

#### Using range

```python
from madmac import MacGenerator

start = '00-B0-A0'
stop = '00-B0-DF'
macg = MacGenerator(start=start, stop=stop)
```

#### Using total number

```python
from madmac import MacGenerator

macg = MacGenerator(total=100)
```

Can be used with `start`:

```python
from madmac import MacGenerator

macg = MacGenerator(start='CC:D1:00', total=100)
```
