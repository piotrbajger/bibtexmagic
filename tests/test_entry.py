import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bibtexmagic.bibtexmagic.entry import BibTexEntry

class TestEntry(unittest.TestCase):
    def setUp(self):
        pass

    def test_parse_entry(self):
        entry_type = "type"
        field_name1 = "title"
        field_name2 = "unsupported"
        field_val1 = "val1"
        field_val2 = "val2"
        entry_key = "key"

        test_entry = ("{entry_type}{{{entry_key},\n" \
            + "\t{field_name1} = {{{field_val1}}},\n" \
            + "\t{field_name2} = {{{field_val2}}},\n" \
        + "}}").format(entry_type=entry_type,
                 field_name1=field_name1,
                 field_name2=field_name2,
                 field_val1=field_val1,
                 field_val2=field_val2,
                 entry_key=entry_key)

        parser_options = None

        #Should raised a warning due to an unsupported field name.
        with self.assertWarns(UserWarning):
            entry = BibTexEntry(test_entry, parser_options)

        self.assertEqual(entry.key, entry_key)
        self.assertEqual(entry.entry_type, entry_type)
        self.assertEqual(len(entry.fields), 1)

if __name__ == "__main__":
    unittest.main()
