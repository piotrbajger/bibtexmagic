import warnings
import sys
import re
import json

class BibTexMagic():
    regular_types = ['article', 'book']

    def __init__(self, pages_double_hyphened=True):
        self.entries = []
        self.pages_double_hyphened = pages_double_hyphened

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

    def parse_field(self, field_name, field_value):
        print(field_name)
        if field_name == "author":
            return self.parse_field_author(field_value)
        elif field_name == "title":
            return self.parse_field_title(field_value)
        elif field_name == "pages":
            return self.parse_field_pages(field_value)

        return field_value


    def parse_field_author(self, field_value):
        author_list = field_value.split(" and ")

        #TBA: Parse von, Jr, etc.. Make sure the names are
        #in the A.B. Surname, {prefix} format

        return author_list

    def parse_field_title(self, field_value):
        par = self.get_parentheses(field_value)

        to_return = ""
        pos = 0
        for key in sorted(par):
            to_return += field_value[pos:key].lower()
            to_return += field_value[(key+1):par[key]]
            pos = par[key]+1

        to_return += field_value[pos:]
        to_return = to_return[0].upper() + to_return[1:]

        return to_return

    def parse_field_pages(self, field_value):
        if self.pages_double_hyphened:
            return re.sub("-{1,2}", "--", field_value)

        return field_value

    def parse_entry(self, entry_raw):
        end_type = entry_raw.find('{')
        entry_type = entry_raw[1:end_type].lower()

        if entry_type not in self.regular_types:
            warnings.warn('Entry type \'' + entry_type + '\' not supported.')
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

                field_val_start = entry_raw.find('{', field_name_end) + 1
                field_val_end = entry_raw.find('},', field_val_start)

                field_parsed = self.parse_field(field_name, entry_raw[field_val_start:field_val_end])

                field_val = field_parsed

                prev_end = field_val_end

                entry[field_name] = field_val

        return entry


    def get_parentheses(self, s):
        to_return = {}
        pstack = []

        for i, c in enumerate(s):
            if c == '{':
                pstack.append(i)
            elif c == '}':
                if not pstack:
                    raise IndexError("No matching opening parenthesis for " + str(i))
                to_return[pstack.pop()] = i

        if pstack:
            raise IndexError("No matching closing parenthesis for " + str(pstack.pop()))

        return to_return


if __name__ == "__main__":
    parser = BibTexMagic()

    parser.parse_bib('bib.bib')

    json.dump(parser.entries, sys.stdout, indent=4, separators=(',', ': '))
