# Pydemonstrativos
Demonstrativos Financeiros - Dados CVM
#### Dependencies
You need Python 3.7 or later to use **pacotepypi**. You can find it at [python.org](https://www.python.org/).You also need setuptools, wheel and twine packages, which is available from [PyPI](https://pypi.org). If you have pip, just run:
```
pip install pandas
```
#### Installation
Clone this repo to your local machine using:
```
git clone https://github.com/andremsilveira/pydemonstrativos
```
## Features
- File structure for PyPI packages
- Setup with package informations
- License example
## Example
```
pip install pydemonstrativo
from pydemonstrativo import CVM

CVM.about()
links = CVM.create_links_api(2012, 2021)
print(links)
```
