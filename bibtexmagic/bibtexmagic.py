import warnings

from .latextouni import LatexToUni
from .entry import BibTexEntry


class BibTexParserOptions():
    """Stores common settings for the parser."""

    def __init__(self,
                 pages_double_hyphened,
                 latex_to_unicode,
                 ignore_unsupported=True):
        """Init the option file.

        Args:
            pages_double_hyphenedi (bool): Whether to use '-' or '--'
                in the 'pages' BibTex field.
            latex_to_unicode (bool): Whether to convert LaTeX macros
                to unicode when parsing certain BibTeX fields.

        """
        self.pages_double_hyphened = pages_double_hyphened
        self.latex_to_unicode = latex_to_unicode
        self.ignore_unsupported = ignore_unsupported


class BibTexMagic():
    """
    Parser main class for BibTexMagic.

    Static variables:
        ALLOWED_ENTRIES: A list of supported BibTex entries.
        CONVERTER: An instance of LatexToUni converter.

    """

    ALLOWED_ENTRIES = ['article', 'book']
    CONVERTER = LatexToUni()

    ALLOWED_FIELDS = {
        'article': {
            'required': ['author', 'title', 'journal', 'year'],
            'optional': ['volume', 'number', 'pages', 'month']
        },
        'book': {
            'required': [['author', 'editor'], 'title', 'publisher', 'year'],
            'optional': [['volume', 'number'], 'series', 'address', 'edition',
                         'month']
        }
    }

    @staticmethod
    def get_fields_for_entry(entry_type, optional=False):
        """Returns a list of fields allowed for a given entry."""
        if entry_type not in BibTexMagic.ALLOWED_ENTRIES:
            raise ValueError(f"Entry type {entry_type} is not supported.")

        if optional:
            return (BibTexMagic.ALLOWED_FIELDS[entry_type]['required'] +
                    BibTexMagic.ALLOWED_FIELDS[entry_type]['optional'])
        else:
            return BibTexMagic.ALLOWED_FIELDS[entry_type]['required']

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

    def parse_bib(self, filename_or_buffer):
        """
        Parses a BibTeX file. Parsed file is then available
        in the 'entries' member variable.

        Args:
            filename_or_buffer: Name of the file to be parsed or a buffer.

        """
        if type(filename_or_buffer) == str:
            with open(filename) as bibfile:
                bib_raw = bibfile.read()
        else:
            try:
                bib_raw = filename_or_buffer.read()
                bib_raw = bib_raw.decode()
            except AttributeError:
                raise ValueError("Need to provide a string (filename) " +
                                 "or a file buffer!")

        entries_unparsed = bib_raw.split("@")

        warnings.simplefilter('always')

        for unparsed in entries_unparsed:
            # Ignore comments
            if unparsed[0] == "%":
                continue

            entry = BibTexEntry(self.options, unparsed)

            if entry is not None:
                self.entries.append(entry)

    def to_json(self):
        """Returns the Bibliography as a JSON string."""
        jsoned = '{\"bibliography\": {\n'
        for entry in self.entries:
            jsoned += entry.to_json()

        # Remove trailing comma
        jsoned = jsoned[:-2] + "\n"

        jsoned += r'}}'

        if self.options.latex_to_unicode:
            jsoned = self.latex_to_unicode(jsoned)
        else:
            jsoned = self.unicode_to_latex(jsoned)

        return jsoned

    def to_bibtex(self):
        """Returns the bibliography as a BibTeX string."""
        bibtexed = ""
        for entry in self.entries:
            bibtexed += "\n\n"
            bibtexed += entry.to_bibtex()

        if self.options.latex_to_unicode:
            bibtexed = self.latex_to_unicode(bibtexed)
        else:
            bibtexed = self.unicode_to_latex(bibtexed)

        return bibtexed
