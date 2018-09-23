from bibtexmagic.fields.field import BibField
from bibtexmagic.bibtexmagic import BibTexMagic

class AuthorBibField(BibField):

    def __init__(self, field_raw, parser_options):
        self.name = "author"
        self.value = self.parse_field(field_raw, parser_options)

    def parse_field(self, field_raw, parser_options):
        """
        Accepts a string containing author names. Names
        are assumed to be separated by " and ". Supports
        the names in the following forms:
            von Last, Jr, First
            First von Last

        Positional arguments:
            field_value -- string with and-separated author names.

        Return value:
        A list of triplets of the form (von Last, Jr, First).
        """

        if parser_options.latex_to_unicode:
            field_raw = BibTexMagic.latex_to_unicode(field_raw)

        author_list = field_raw.split(" and ")

        for i, author in enumerate(author_list):
            author_list[i] = self._parse_author_name(author)

        return author_list


    def _parse_author_name(self, author):
        """
        Parses single author name.

        Positional arguments:
        author -- string containing author name.
            von Last, Jr, First, or
            First von Last

        Return value:
        A triplet of the form (von Last, Jr, First).
        """

        #For comma-separated entries
        if "," in author:
            parts = [part.strip() for part in author.split(",")]

            last = parts[0]
            first = parts[-1]
            jr = ""

            if len(parts) > 3:
                jr = parts[1]

        else:
            parts = [part.strip() for part in author.split()]
            lower = None

            for i, part in enumerate(parts):
                if part[0].islower():
                    lower = i
                    break

            if lower is not None:
                last = " ".join(parts[lower:])
                first = " ".join(parts[:lower])
                jr = ""
            else:
                last = parts[-1]
                first = " ".join(parts[:-1])
                jr = ""

        return [last, jr, first]



