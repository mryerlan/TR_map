# TR MAP Version 2.0

This project makes a sequence of all transport nodes for each base station. 
Based on the mac address table and routing tables

List of supported equipment:
* Mini-Link TN
* Mini-Link CN210
* Mini-Link 6352
* Mini-Link 6000
* Optix RTN 900
* Optix RTN 300

List of required reports

SoEM:
* Ne inventory
* Ne ethernet

NCE
* Cable report
* NE report
* Self mac address report

## Installation

Use the package manager [pip](https://www.python.org/downloads/release/python-390/) to install foobar.

```bash
pip install python3.9
```

## Usage

```python

import re
import zipfile

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)