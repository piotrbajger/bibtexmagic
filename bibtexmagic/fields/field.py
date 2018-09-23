from importlib import import_module

class BibField():
    """
    Represents a generic BibTtex field. Base class for fields
    requiring special parsing.

    Variables:
        _ALLOWED_FIELDS -- a list of allowed field names.
    """

    _ALLOWED_FIELDS = ['address', 'annote', 'author', 'booktitle', 'chapter',
        'crossref', 'edition', 'editor', 'file', 'howpublished', 'institution',
        'journal', 'key', 'month', 'note', 'number', 'organization', 'pages',
        'publisher', 'school', 'series', 'title', 'type', 'volume', 'year']


    @staticmethod
    def create_field(field_name, field_raw, parser_options):
        """
        Parses raw field text and creates an appropriate object.

        Positional arguments:
        field_name -- name of the field (e.g. Author or Journal)
        field_raw -- an unparsed string containing the field value.
        parser_options -- an instance of BibTexParserOptions.

        Return value:
        A concrete instance derived from BibField object. None if
        field field_name is not implemented.
        """
        field = None
        class_name = field_name.capitalize() + 'BibField'

        try:
            field_module = import_module('bibtexmagic.fields.' + field_name.lower())

            field = getattr(field_module, class_name)(field_raw, parser_options)
        except ImportError:
            if field_name.lower() in BibField._ALLOWED_FIELDS:
                field = BibField(field_name, field_raw)

        return field


    def __init__(self, field_name, field_raw):
        self.name = field_name
        self.value = field_raw

    def parse_field(self, field_raw, parser_options):
        """Field-specific parser."""
        return field_raw

    def __str__(self):
        return "{} = {},".format(self.name, self.value)
