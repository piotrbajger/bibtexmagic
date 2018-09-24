import re

from .field import BibTexField
from ..bibtexmagic import BibTexMagic

class PagesBibTexField(BibTexField):

    def __init__(self, field_raw, parser_options):
        self.name = "pages"
        self.value = self.parse_field(field_raw, parser_options)

    def parse_field(self, field_raw, parser_options):
        if parser_options.pages_double_hyphened:
            return re.sub("-{1,2}", "--", field_raw)
        else:
            return field_raw.replace("--", "-")

