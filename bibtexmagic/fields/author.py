from .field import BibTexField
from ..bibtexmagic import BibTexMagic

class AuthorBibTexField(BibTexField):
    """Class representing the Author field."""

    def __init__(self, field_raw, parser_options):
        """Initialises and parses the field.

        Args:
            field_raw (str): Raw BibTex string as seen in a BibTeX file.
            parser_options: An instance of BibTexParserOptions.

        """
        self.name = "author"
        self.value = self.parse_field(field_raw, parser_options)

    def parse_field(self, field_raw, parser_options):
        """Parses the field.

        Accepts a string containing author names. Names are assumed to be
        separated by " and ". Supports the names in the following forms:
            von Last, Jr, First
            First von Last

        Args:
            field_raw (str): Raw BibTex string as seen in a BibTeX file.
            parser_options: An instance of BibTexParserOptions.

        Returns:
            list: A list of triplets of the form (von Last, Jr, First).

        """
        if parser_options.latex_to_unicode:
            field_raw = BibTexMagic.latex_to_unicode(field_raw)

        author_list = field_raw.split(" and ")

        for i, author in enumerate(author_list):
            author_list[i] = self._parse_author_name(author)

        return author_list


    def _parse_author_name(self, author):
        """Parses a single author name.

        Args:
            author (str): String containing author name.
                Assumes following formats: 'von Last, Jr, First', or
                'First von Last'.

        Returns:
            A triplet of the form (von Last, Jr, First).

        """
        #For comma-separated entries
        if "," in author:
            parts = [part.strip() for part in author.split(",")]

            last = parts[0]
            first = parts[-1]
            jr = ""

            if len(parts) > 2:
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


    def to_json(self):
        """Returns the entry as a JSON string.

        """
        jsoned = "\t\t\t\"author\": [\n"

        for author in self.value:
            jsoned += "\t\t\t\t"
            jsoned += "{{\"first\": \"{}\", ".format(author[0])
            jsoned += "\"jr\": \"{}\", ".format(author[1])
            jsoned += "\"last\": \"{}\"}},\n".format(author[2])

        #Remove trailing comma
        jsoned = jsoned[:-2] + "\n"
        jsoned += "\t\t\t],\n"
        return jsoned

    def to_bibtex(self):
        """Returns the author field as a BibTeX string."""
        bibtexed = "author = {"
        for author in self.value:
            if author[1] != "":
                bibtexed += "{}, {}, {} and ".format(*author)
            else:
                bibtexed += "{}, {} and ".format(author[0], author[2])

        #Remove trailing ' and '.
        bibtexed = bibtexed[:-5] + "}"

        return bibtexed


