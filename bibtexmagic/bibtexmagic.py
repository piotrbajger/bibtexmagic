import warnings
import sys
import re
import json

from bibtexmagic.latextouni import LatexToUni
from bibtexmagic.fields.field import BibField
from bibtexmagic.entry import BibTexEntry

class BibTexParserOptions():
    """Stores common settings for the parser."""

    def __init__(self,
                 pages_double_hyphened,
                 latex_to_unicode
                ):
        self.pages_double_hyphened = pages_double_hyphened
        self.latex_to_unicode = latex_to_unicode


class BibTexMagic():
    """
    Parser main class for BibTexMagic.
        ALLOWED_ENTRIES: a list of supported BibTex entries.
    """

    ALLOWED_ENTRIES = ['article', 'book']

    converter = LatexToUni()

    @staticmethod
    def latex_to_unicode(text):
        return BibTexMagic.converter.lat_to_uni(text)

    def __init__(self,
                 pages_double_hyphened=True,
                 latex_to_unicode=True,
                ):
        """
        Initialise a new parser with a set of options.

        Keyword arguments:
        pages_double_hyphened -- if True, two hyphens are used to set page
            numbers. If False, one is used instead. Default: True
        latex_to_unicode -- if True, LaTeX macros are converted to
            unicode characters (e.g. \'{o} becomes ó). If False, the macro
            strings are retained as is. Default: True.
        """

        self.entries = []

        self.options = BibTexParserOptions(pages_double_hyphened,
                                           latex_to_unicode
                                          )

    def parse_bib(self, filename):
        """
        Parses a BibTeX file. The file is then stored internally
        in the entries member variable.

        Positional arguments:
        filename -- file name to be parsed.
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
            return None
        else:
            for entry in self.entries:
                print(str(entry) + "\n")

#Keep it here for now for testing purposes
if __name__ == "__main__":
    parser = BibTexMagic()

    parser.parse_bib('bibtexmagic/bib.bib')

    parser.to_text()
