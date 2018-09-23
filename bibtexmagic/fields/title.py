from bibtexmagic.fields.field import BibField
from bibtexmagic.bibtexmagic import BibTexMagic
from bibtexmagic.helper import get_parentheses

class TitleBibField(BibField):

    def __init__(self, field_raw, parser_options):
        self.name = "title"
        self.value = self.parse_field(field_raw, parser_options)

    def parse_field(self, field_raw, parser_options):
        if parser_options.latex_to_unicode:
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

        return to_return
