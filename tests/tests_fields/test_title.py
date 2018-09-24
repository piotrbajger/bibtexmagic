import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bibtexmagic.bibtexmagic.fields import title, field
from bibtexmagic.bibtexmagic.bibtexmagic import BibTexParserOptions


class TestTitleField(unittest.TestCase):
    def setUp(self):
        self.parser_options = BibTexParserOptions(
            pages_double_hyphened=False,
            latex_to_unicode=False)

    def test_create_field(self):
        f1 = field.BibTexField.create_field(
                "title", "simple title", self.parser_options)

        #Tests correct type
        self.assertTrue(isinstance(f1, title.TitleBibTexField))


    def test_parse_field(self):
        titles_raw = ["simple title", "simple {TITLE}"]
        titles = ["Simple title", "Simple TITLE"]

        for raw, parsed in zip(titles_raw, titles):
            f = field.BibTexField.create_field(
                "title", raw, self.parser_options)

            self.assertEqual(f.name, "title")
            self.assertEqual(f.value, parsed)
