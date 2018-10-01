[![pipeline status](https://gitlab.com/piotrbajger/bibtexmagic/badges/master/pipeline.svg)](https://gitlab.com/piotrbajger/bibtexmagic/commits/master)
[![Documentation Status](https://readthedocs.org/projects/bibtexmagic/badge/?version=latest)](https://bibtexmagic.readthedocs.io/en/latest/?badge=latest)

# BibTeXMagic

BibTeXMagic is a parser for BibTeX providing a Python interface to interact with bibliography databases. It currently supports convertions from BibTeX to JSON and execution of LaTeX macros for special characters commonly occurring in paper titles or author names (e.g. greek letters or diacritical signs).

The project is currently in its alpha version. See [here](https://bibtexmagic.readthedocs.io/en/latest/) for full documentation.

## Installation

The instructions below will allow you to get a copy of the project.

To install BibTeXMagic using pip simply clone this repository:
```
git clone https://gitlab.com/piotrbajger/bibtexmagic.git
cd bibtexmagic
pip install .
```

To verify that the BibTeXMagic works as intended, run the unit tests from the bibtexmagic folder:
```
nosetests -v
```

## Usage

Assuming that your bibliography file is called "bibliography.bib", you can use BibTeXMagic to parse it as follows:
```
from bibtexmagic.bibtexmagic import BibTexMagic

parser = BibTexMagic() # Define the parser with the default options
parser.parse_bib("bibliography.bib") # Parse the bibliography file
```
You can then use the conversion functions to return the bibliography in a prefered format, e.g.: 
```
parser.to_json() # Prints the bibliography file in the JSON format.
```
You may adjust the output to your preferences by toggling flags in parser.options, e.g.:
```
parser.options.latex_to_unicode = True
parser.to_bibtex() # Prints back the BibTeX file but with unicode characters
                   # rather than LaTeX macros.
```

## Authors

This project is maintained by [*Piotr bajger*](https://gitlab.com/piotrbajger).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details





