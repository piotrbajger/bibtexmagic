import warnings
import sys
import re
import json

from .latextouni import LatexToUni
from .fields.field import BibTexField
from .entry import BibTexEntry

class BibTexParserOptions():
    """Stores common settings for the parser."""

    def __init__(self,
                 pages_double_hyphened,
                 latex_to_unicode):
        """Init the option file.

        Args:
            pages_double_hyphenedi (bool): Whether to use '-' or '--'
                in the 'pages' BibTex field.
            latex_to_unicode (bool): Whether to convert LaTeX macros
                to unicode when parsing certain BibTeX fields.

        """
        self.pages_double_hyphened = pages_double_hyphened
        self.latex_to_unicode = latex_to_unicode


class BibTexMagic():
    """
    Parser main class for BibTexMagic.

    Static variables:
        ALLOWED_ENTRIES: A list of supported BibTex entries.
        CONVERTER: An instance of LatexToUni converter.

    """

    ALLOWED_ENTRIES = ['article', 'book']
    CONVERTER = LatexToUni()

    @staticmethod
    def latex_to_unicode(text):
        """
        Parses the LaTeX diacritic character macros and converts
        them to unicode characters, e.g. ą --> \'{a}.

        Args:
            text (str): Text to be converted.

        Returns:
            str: Converted text.

        """
        return BibTexMagic.CONVERTER.lat_to_uni(text)


    @staticmethod
    def unicode_to_latex(text):
        """
        Parses a unicode text and converts diacritic signs to the corresponding
        LaTeX macros, e.g. \'{a} --> ą.

        Args:
            text (str): Text to be converted.

        Returns:
            str: Converted text.

        """

        return BibTexMagic.CONVERTER.uni_to_lat(text)


    def __init__(self,
                 pages_double_hyphened=True,
                 latex_to_unicode=True):
        """
        Initialise a new parser with a set of options.

        Args:
            pages_double_hyphened (bool): If True, two hyphens are used to set
                page numbers. If False, one is used instead. Default: True
            latex_to_unicode(bool): If True, LaTeX macros are converted to
                unicode characters (e.g. \'{o} becomes ó). If False, the macro
                strings are retained as is. Default: True.
        """

        self.entries = []

        self.options = BibTexParserOptions(pages_double_hyphened,
                                           latex_to_unicode)


    def parse_bib(self, filename):
        """
        Parses a BibTeX file. Parsed file is then available
        in the 'entries' member variable.

        Args:
            filename (str): Name of the file to be parsed.

        """

        with open(filename) as bibfile:
            bib_raw = bibfile.read()

        entries_unparsed = bib_raw.split("@")

        warnings.simplefilter('always')

        for unparsed in entries_unparsed:
            #Ignore comments
            if unparsed[0] == "%": continue

            entry = BibTexEntry(unparsed, self.options)

            if entry is not None:
                self.entries.append(entry)


    def to_text(self):
        """Prints a parsed file into a more readable format."""
        if not self.entries:
            warnings.warn("A BibTeX file has not been parsed yet.")
        else:
            for entry in self.entries:
                print(str(entry) + "\n")
