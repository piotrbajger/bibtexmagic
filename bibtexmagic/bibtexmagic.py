from .latextouni import LatexToUni
from .entry import BibTexEntry


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

    def __init__(self):
        """
        Initialise a new parser.
        """

        self.entries = []

    def parse_bib(self, filename_or_buffer):
        """
        Parses a BibTeX file. Parsed file is then available
        in the 'entries' member variable.

        Args:
            filename_or_buffer: Name of the file to be parsed or a buffer.

        """
        if type(filename_or_buffer) == str:
            with open(filename_or_buffer) as bibfile:
                bib_raw = bibfile.read()
        else:
            try:
                bib_raw = filename_or_buffer.read()
                bib_raw = bib_raw.decode()
            except AttributeError:
                raise ValueError("Need to provide a string (filename) " +
                                 "or a file buffer!")

        entries_unparsed = bib_raw.split("@")

        for unparsed in entries_unparsed:
            # Ignore comments
            if unparsed[0] == "%":
                continue

            entry = BibTexEntry(unparsed)

            if entry is not None:
                self.entries.append(entry)

    def to_bibtex(self):
        """Returns the bibliography as a BibTeX string."""
        bibtexed = ""
        for entry in self.entries:
            bibtexed += "\n\n"
            bibtexed += entry.to_bibtex()

        bibtexed = self.latex_to_unicode(bibtexed)

        return bibtexed
