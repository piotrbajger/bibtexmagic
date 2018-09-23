import re

from bibtexmagic.fields.field import BibField
from bibtexmagic.bibtexmagic import BibTexMagic

class PagesBibField(BibField):

    def __init__(self, field_raw, parser_options):
        self.name = "pages"
        self.value = self.parse_field(field_raw, parser_options)

    def parse_field(self, field_raw, parser_options):
        if parser_options.pages_double_hyphened:
            return re.sub("[\s]+-{1,2}[\s]+", "--", field_raw)
        else:
            field_raw.replace("--", "-")
            return re.sub("[\s]+-[\s]+", "-", field_raw)

