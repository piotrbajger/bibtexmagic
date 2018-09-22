import warnings
import sys
import re
import json

from latextouni import LatexToUni


class BibTexMagic():
    ALLOWED_ENTRIES = ['article', 'book']
    ALLOWED_FIELDS = ['address', 'annote', 'author', 'booktitle', 'chapter',
        'crossref', 'edition', 'editor', 'file', 'howpublished', 'institution', 'journal',
        'key', 'month', 'note', 'number', 'organization', 'pages', 'publisher',
        'school', 'series', 'title', 'type', 'volume', 'year']

    def __init__(self, pages_double_hyphened=True, latex_to_unicode=True, restrict_to_allowed=True):
        self.entries = []

        self.converter = LatexToUni()

        self.pages_double_hyphened = pages_double_hyphened
        self.restrict_to_allowed = restrict_to_allowed
        self.latex_to_unicode = latex_to_unicode

    def parse_bib(self, filename):
        with open(filename) as bibfile:
            bib_raw = bibfile.read()

        found_prev = bib_raw.find('@')

        warnings.simplefilter('always')

        while found_prev > -1:
            found_next = bib_raw.find('@', found_prev+1)

            entry_raw = (bib_raw[found_prev:found_next])

            with warnings.catch_warnings(record=False):
                entry = self.parse_entry(entry_raw)

            found_prev = found_next

            if entry is not None:
                self.entries.append(entry)


    def parse_entry(self, entry_raw):
        end_type = entry_raw.find('{')
        entry_type = entry_raw[1:end_type].lower()

        if self.restrict_to_allowed or entry_type not in self.ALLOWED_ENTRIES:
            warnings.warn('Entry type {} not supported.'.format(entry_type))
            return None

        entry = {}

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
        if field_name == "author":
            return self.parse_field_author(field_value)
        elif field_name == "title":
            return self.parse_field_title(field_value)
        elif field_name == "pages":
            return self.parse_field_pages(field_value)

        return field_value


    def parse_field_author(self, field_value):
        if self.latex_to_unicode:
            field_value = self.converter.lat_to_uni(field_value)

        author_list = field_value.split(" and ")

        for i, author in enumerate(author_list):
            author_list[i] = self._parse_author_name(author)

        return author_list

    def _parse_author_name(self, author):
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
        if self.pages_double_hyphened:
            return re.sub("-{1,2}", "--", field_value)
        else:
            return field_value.replace("--", "-")

    def get_parentheses(self, s, stop_on_closing=False):
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

    def convert_to_utf(self, s):
        pass

#Keep it here for now for testing purposes
if __name__ == "__main__":
    parser = BibTexMagic(restrict_to_allowed=False)

    parser.parse_bib('bib.bib')

    json.dump(parser.entries, sys.stdout, indent=4, separators=(',', ': '))
