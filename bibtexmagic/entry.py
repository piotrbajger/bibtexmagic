import re
import warnings

from .helper import get_parentheses
from .fields.field import BibField

class BibTexEntry():
    def __init__(self, entry_raw, parser_options):
        """
        Initialises an entry from BibTex string.

        Arguments:
        entry_raw: a BibTex string to be parsed.
        parser_options: an instance of BibTexParserOptions
        """

        self.entry_type = None
        self.key = None

        self.fields = []

        self.parse_entry(entry_raw, parser_options)


    def parse_entry(self, entry_raw, parser_options):
        """
        Does the actual parsing and fills the member variables in.

        Positional arguments:
        entry_raw -- text containing a BibTeX entry
        """

        end_type = entry_raw.find('{')
        self.entry_type = entry_raw[:end_type].lower()

        end_key = entry_raw.find(',', end_type+1)
        self.key  = entry_raw[(end_type+1):end_key]

        prev_end = end_key

        while True:
            find_field = re.search('\w', entry_raw[prev_end:])

            if find_field is None:
                break

            field_start = prev_end + find_field.start()

            field_name_end = entry_raw.find('=', field_start)

            field_name = entry_raw[field_start:field_name_end].strip()

            field_val_start = entry_raw.find('{', field_name_end)
            field_val_end = field_val_start + get_parentheses(entry_raw[field_val_start:], True)[0]

            field_raw = entry_raw[(field_val_start+1):field_val_end]

            field = BibField.create_field(field_name, field_raw, parser_options)

            prev_end = field_val_end

            if field is not None:
                self.fields.append(field)
            else:
                warnings.warn('Field {} not supported'.format(field_name))

    def __str__(self):
        to_return = "{} ({})\n".format(self.key, self.entry_type)
        for field in self.fields:
            to_return += "\t" + str(field) + "\n"

        return to_return
