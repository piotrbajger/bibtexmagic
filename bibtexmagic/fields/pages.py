import re

from .field import BibTexField


class PagesBibTexField(BibTexField):
    """Class representing a 'pages' BibTeX field."""

    def __init__(self, field_raw):
        """Initialises and parses the field.

        Args:
            field_raw (str): Raw BibTex string as seen in a BibTeX file.

        """
        self.name = "pages"
        self.value = self.parse_field(field_raw)

    def parse_field(self, field_raw):
        """Parses the field.

        Args:
            field_raw (str): Raw BibTex string as seen in a BibTeX file.

        Returns:
            Parsed field in a form XXX-YYY or XXX--YYY.

        """
        return re.sub("-{1,2}", "--", field_raw)
