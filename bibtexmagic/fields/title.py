from .field import BibTexField
from ..bibtexmagic import BibTexMagic
from ..helper import get_parentheses


class TitleBibTexField(BibTexField):
    """Initialises and parses the field."""

    def __init__(self, field_raw):
        """Initialises and parses the field.

        Args:
            field_raw (str): Raw BibTex string as seen in a BibTeX file.

        """
        self.name = "title"
        self.value = self.parse_field(field_raw)

    def parse_field(self, field_raw):
        """Parses the field.

        Respectes capital letters in {} brackets and parses LaTeX
        macros dependeing on 'parser_options'.

        Args:
            field_raw (str): Raw BibTex string as seen in a BibTeX file.
            parser_options: An instance of BibTexParserOptions.

        Returns:
            A parsed title.

        """
        field_raw = BibTexMagic.latex_to_unicode(field_raw)

        par = get_parentheses(field_raw)

        to_return = ""
        pos = 0
        for key in sorted(par):
            to_return += field_raw[pos:key].lower()
            to_return += field_raw[(key+1):par[key]]
            pos = par[key]+1

        to_return += field_raw[pos:].lower()
        to_return = to_return[0].upper() + to_return[1:]

        to_return = BibTexMagic.unicode_to_latex(to_return)

        return to_return
