import warnings
import re

class BibTexMagic():
    regular_types = ['article', 'book']

    def __init__(self):
        self.entries = [];


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

                field_val_start = entry_raw.find('{', field_name_end)
                field_val_end = entry_raw.find('},', field_val_start)

                field_val = entry_raw[(field_val_start+1):field_val_end]
                prev_end = field_val_end

                entry[field_name] = field_val

        return entry

if __name__ == "__main__":
    parser = BibTexMagic()

    parser.parse_bib('bib.bib')

    print(parser.entries)
