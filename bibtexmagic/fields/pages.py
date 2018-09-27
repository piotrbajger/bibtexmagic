import re

from .field import BibTexField
from ..bibtexmagic import BibTexMagic

class PagesBibTexField(BibTexField):
    """Class representing a 'pages' BibTeX field."""

    def __init__(self, field_raw, parser_options):
        """Initialises and parses the field.

        Args:
            field_raw (str): Raw BibTex string as seen in a BibTeX file.
            parser_options: An instance of BibTexParserOptions.

        """
        self.name = "pages"
        self.value = self.parse_field(field_raw, parser_options)


    def parse_field(self, field_raw, parser_options):
        """Parses the field.

        Args:
            field_raw (str): Raw BibTex string as seen in a BibTeX file.
            parser_options: An instance of BibTexParserOptions.

        Returns:
            Parsed field in a form XXX-YYY or XXX--YYY.

        """
        if parser_options.pages_double_hyphened:
            return re.sub("-{1,2}", "--", field_raw)
        else:
            return field_raw.replace("--", "-")

