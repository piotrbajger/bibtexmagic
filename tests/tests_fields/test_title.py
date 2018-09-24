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

            self.assertTrue(f.name, "title")
            self.assertTrue(f.value, parsed)

    def test_parse_field_unicode(self):
        title_raw = "title with macr\'{o}"
        parsed_no_uni = "title with macr" + u"00F3"
        parsed_uni = "title with macr" + u"00F3"

        #Should not parse unicode
        f = field.BibTexField.create_field(
            "title", title_raw, self.parser_options)

        self.assertTrue(f.value, parsed_no_uni)

        #Now should start parsing unicode
        self.parser_options.latex_to_unicode = True

        f = field.BibTexField.create_field(
            "title", title_raw, self.parser_options)

        self.assertTrue(f.value, parsed_uni)
