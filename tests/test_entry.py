import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bibtexmagic.bibtexmagic.entry import BibTexEntry
from bibtexmagic.bibtexmagic.bibtexmagic import BibTexParserOptions

class TestEntry(unittest.TestCase):
    def setUp(self):
        self.parser_options = BibTexParserOptions(
            pages_double_hyphened=False,
            latex_to_unicode=False)

        self.entry_type = "type"
        self.field_name1 = "title"
        self.field_name2 = "unsupported"
        self.field_val1 = "{VAL1}"
        self.field_val2 = "val2"
        self.entry_key = "key"

        self.test_entry = ("{entry_type}{{{entry_key},\n" \
            + "\t{field_name1} = {{{field_val1}}},\n" \
            + "\t{field_name2} = {{{field_val2}}},\n" \
            + "}}").format(
                 entry_type=self.entry_type,
                 field_name1=self.field_name1,
                 field_name2=self.field_name2,
                 field_val1=self.field_val1,
                 field_val2=self.field_val2,
                 entry_key=self.entry_key)


    def test_parse_entry(self):
        entry = BibTexEntry(self.parser_options)

        #Should raise a warning due to an unsupported field name.
        with self.assertRaises(UserWarning):
            entry.parse_entry(self.test_entry, self.parser_options)

        self.assertEqual(entry.key, self.entry_key)
        self.assertEqual(entry.entry_type, self.entry_type)
        self.assertEqual(len(entry.fields), 1)

if __name__ == "__main__":
    unittest.main()
