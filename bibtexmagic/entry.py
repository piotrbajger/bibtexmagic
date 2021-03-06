import re

from .helper import get_parentheses
from .fields.field import BibTexField


class BibTexEntry():
    """Internal class storing a single BibTeX entry like 'Article'."""

    def __init__(self, entry_raw=None):
        """
        Initialises an entry from BibTex string.

        Args:
            entry_raw (str): A BibTex string to be parsed.
        """

        self.entry_type = None
        self.key = None

        self.fields = []

        if entry_raw is not None:
            self.parse_entry(entry_raw)

    def parse_entry(self, entry_raw):
        """
        Does the actual parsing and fills in the 'fields' member variable.

        Args:
            entry_raw (str): Text containing a BibTeX entry.
            parser_options: An instance of BibTexParserOptions.

        """
        end_type = entry_raw.find('{')
        self.entry_type = entry_raw[:end_type].lower()

        end_key = entry_raw.find(',', end_type+1)
        self.key = entry_raw[(end_type+1):end_key]

        prev_end = end_key

        while True:
            find_field = re.search(r'\w', entry_raw[prev_end:])

            if find_field is None:
                break

            field_start = prev_end + find_field.start()

            field_name_end = entry_raw.find('=', field_start)

            field_name = entry_raw[field_start:field_name_end].strip()

            field_val_start = entry_raw.find('{', field_name_end)
            field_val_end = field_val_start + \
                get_parentheses(entry_raw[field_val_start:], True)[0]

            field_raw = entry_raw[(field_val_start+1):field_val_end]

            field = BibTexField.create_field(field_name, field_raw)

            prev_end = field_val_end

            if field is not None:
                self.fields.append(field)

    def to_dict(self):
        """Returns the entry as Python dictionary"""
        ret_dict = {}

        for f in self.fields:
            ret_dict[f.name] = f.to_string()

        return ret_dict

    def to_bibtex(self):
        """Returns the entry as a BibTeX string."""
        bibtexed = "@{}{{{},\n".format(self.entry_type, self.key)
        for field in self.fields:
            bibtexed += "\t" + field.to_bibtex() + ",\n"
        bibtexed += "}"

        return bibtexed
