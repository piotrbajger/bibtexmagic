import warnings
import sys
import re
import json

from latextouni import LatexToUni

class BibTexMagic():
    """
    Parser main class for BibTexMagic.
    Static variables:
        ALLOWED_ENTRIES: a list of supported BibTex entries.
        ALLOWED_FIELDS: a list of allowed BibTex fields.
    """

    ALLOWED_ENTRIES = ['article', 'book']

    ALLOWED_FIELDS = ['address', 'annote', 'author', 'booktitle', 'chapter',
        'crossref', 'edition', 'editor', 'file', 'howpublished', 'institution', 'journal',
        'key', 'month', 'note', 'number', 'organization', 'pages', 'publisher',
        'school', 'series', 'title', 'type', 'volume', 'year']


    def __init__(self, pages_double_hyphened=True, latex_to_unicode=True, restrict_to_allowed=True):
        """
        Initialise a new parser with a set of options.

        Keyword arguments:
        pages_double_hyphened -- if True, two hyphens are used to set page
            numbers. If False, one is used instead. Default: True
        latex_to_unicode -- if True, LaTeX macros are converted to
            unicode characters (e.g. \'{o} becomes ó). If False, the macro
            strings are retained as is. Default: True.
        restrict_to_allowed -- if True, only fields from the ALLOWED_FIELDS
            list are parsed. If False, all fields are parsed. Default: True.
        """

        self.entries = []

        self.converter = LatexToUni()

        self.pages_double_hyphened = pages_double_hyphened
        self.restrict_to_allowed = restrict_to_allowed
        self.latex_to_unicode = latex_to_unicode

    def parse_bib(self, filename):
        """
        Parses a BibTeX file. The file is then stored internally
        in the entries member variable.

        Positional arguments:
        filename -- file name to be parsed.
        """

        with open(filename) as bibfile:
            bib_raw = bibfile.read()

        entries_unparsed = bib_raw.split("@")

        warnings.simplefilter('always')

        for unparsed in entries_unparsed:
            with warnings.catch_warnings(record=False):
                entry = self.parse_entry(unparsed)

            if entry is not None:
                self.entries.append(entry)


    def parse_entry(self, entry_raw):
        """
        Parses a single bibtex entry. Returns a dictionary
        containing entry type (book/article/etc.) and all
        the supported fields. Returns None if entry not
        supported.

        Positional arguments:
        entry_raw -- text containing a BibTeX entry
            (starting with @)
        """

        #Ignore comments
        if entry_raw[0] == "%":
            return None

        end_type = entry_raw.find('{')
        entry_type = entry_raw[:end_type].lower()

        if self.restrict_to_allowed or entry_type not in self.ALLOWED_ENTRIES:
            warnings.warn('Entry type {} not supported.'.format(entry_type))
            return None

        entry = {}
        entry['type'] = entry_type

        if entry_type == 'article':
            end_key = entry_raw.find(',', end_type+1)
            entry['key'] = entry_raw[(end_type+1):end_key]

            prev_end = end_key

            while True:
                find_field = re.search('\w', entry_raw[prev_end:])

                if find_field is None:
                    break

                field_start = prev_end + find_field.start()

                field_name_end = entry_raw.find('=', field_start)

                field_name = entry_raw[field_start:field_name_end].strip()

                field_val_start = entry_raw.find('{', field_name_end)
                field_val_end = field_val_start + self.get_parentheses(entry_raw[field_val_start:], True)[0]

                field_parsed = self.parse_field(field_name, entry_raw[(field_val_start+1):field_val_end])

                field_val = field_parsed

                prev_end = field_val_end

                if not self.restrict_to_allowed or field_name.lower() in self.ALLOWED_FIELDS:
                    entry[field_name] = field_val
                else:
                    warnings.warn('Field {} not supported'.format(field_name))

        return entry


    def parse_field(self, field_name, field_value):
        """
        Parses a single BibTeX field. Calls a field-specific
        parser when required (e.g. author, title).
        """
        if field_name == "author":
            return self.parse_field_author(field_value)
        elif field_name == "title":
            return self.parse_field_title(field_value)
        elif field_name == "pages":
            return self.parse_field_pages(field_value)

        return field_value


    def parse_field_author(self, field_value):
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

        if self.latex_to_unicode:
            field_value = self.converter.lat_to_uni(field_value)

        author_list = field_value.split(" and ")

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



        #Surname first
        if "," in words[0]:
            names = [name[0].upper() + "." for name in words[1:]]
            return words[0][:-1] + ", " + "".join(names)
        else:
            names = [name[0].upper() + "." for name in words[:-1]]
            return words[-1] + ", " + "".join(names)

    def parse_field_title(self, field_value):
        """
        Parses the title field while respecting BibTex {Blocks}.
        LaTeX macros are parsed depending on the latex_to_unicode option.

        Positional arguments:
        field_value -- string containing the title.

        Return value:
        String containing a parsed title.
        """
        if self.latex_to_unicode:
            field_value = self.converter.lat_to_uni(field_value)

        par = self.get_parentheses(field_value)

        to_return = ""
        pos = 0
        for key in sorted(par):
            to_return += field_value[pos:key].lower()
            to_return += field_value[(key+1):par[key]]
            pos = par[key]+1

        to_return += field_value[pos:].lower()
        to_return = to_return[0].upper() + to_return[1:]

        return to_return

    def parse_field_pages(self, field_value):
        """
        Parses the pages field.
        Result is hyphened according to the pages_double_hyphened option.

        Positional arguments:
        field_value -- string containing the pages field value.

        Return value:
        A string containing the the parsed pages field.
        """
        if self.pages_double_hyphened:
            return re.sub("-{1,2}", "--", field_value)
        else:
            return field_value.replace("--", "-")

    def get_parentheses(self, s, stop_on_closing=False):
        """
        Looks up opening/closing parentheses pairs in a string.

        Positional arguments:
        s -- input string.

        Keyword arguments:
        stop_on_closing -- if True, parsing stops upon reaching
            a closing parenthesis of the first opening one. If False,
            the parser continues until the end of the string.

        Return value:
        A dictionary of parentheses positions in a string containing
            entries of the form "opening: closing".
        """
        to_return = {}
        pstack = []

        for i, c in enumerate(s):
            if c == '{':
                pstack.append(i)
            elif c == '}':
                if not pstack:
                    raise IndexError("No matching opening parenthesis for " + str(i))
                to_return[pstack.pop()] = i

                #If all brackets closed, return?
                if stop_on_closing and not pstack:
                    return to_return

        if pstack:
            raise IndexError("No matching closing parenthesis for " + str(pstack.pop()))

        return to_return

    def to_json(self):
        if not entries:
            warnings.warn("A BibTeX file has not been parsed yet.")
            return None
        else:
            json.dumps(entries)

#Keep it here for now for testing purposes
if __name__ == "__main__":
    parser = BibTexMagic(restrict_to_allowed=False)

    parser.parse_bib('bib.bib')

    json.dump(parser.entries, sys.stdout, indent=4, separators=(',', ': '))
