from importlib import import_module
import logging


class BibTexField():
    """
    Represents a generic BibTtex field. Base class for fields
    requiring special parsing.

    Static members:
        _ALLOWED_FIELDS (list): A list of allowed field names.

    """

    _ALLOWED_FIELDS = [
        'address', 'annote', 'author', 'booktitle', 'chapter',
        'crossref', 'edition', 'editor', 'file', 'howpublished', 'institution',
        'journal', 'key', 'month', 'note', 'number', 'organization', 'pages',
        'publisher', 'school', 'series', 'title', 'type', 'volume', 'year'
    ]

    @staticmethod
    def create_field(field_name, field_raw):
        """BibTexField factory.

        Parses raw field text and creates an appropriate object.

        Args:
            field_name (str): Name of the field (e.g. Author or Journal)
            field_raw (str): An unparsed string containing the field value.

        Returns:
            (BibTexField): A concrete instance derived from BibTexField
                object. None if field field_name is not implemented.

        Raises:
            UserWarning if field is not allowed.

        """
        field_name = field_name.lower()
        if (field_name not in BibTexField._ALLOWED_FIELDS):
            raise UserWarning(f"Field {field_name} not supported.")
            return None
        field = None
        class_name = field_name.capitalize() + 'BibTexField'

        try:
            # field_module = import_module(
            #     field_name)
            logging.debug(f"Attempting to import {field_name}.")
            field_module = import_module(f".bibtexmagic.fields.{field_name}",
                                         package="bibtexmagic")
            logging.debug(f"Found field subclass for {field_name}.")

            field = getattr(field_module, class_name)(field_raw)

        except ImportError:
            field = BibTexField(field_name, field_raw)
            logging.debug(f"Creating generic field for {field_name}.")

        return field

    def __init__(self, field_name, field_raw):
        """Initialises the object.

        Args:
            field_name (str): The name of the field, e.g. 'author'.
            field_raw (str): Unparsed field value as seen in a BibTeX file.

        """
        self.name = field_name
        self.value = field_raw

    def parse_field(self, field_raw, parser_options):
        """Field-specific parser."""
        return field_raw

    def to_json(self):
        return "\t\t\t\"{}\": \"{}\",\n".format(self.name, self.value)

    def to_bibtex(self):
        return "{} = {{{}}}".format(self.name, self.value)

    def to_string(self):
        return self.value

    def __repr__(self):
        return f"<{self.name}: {self.value}>"
