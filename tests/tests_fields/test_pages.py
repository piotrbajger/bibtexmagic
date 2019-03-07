import unittest

from bibtexmagic.bibtexmagic.fields import pages, field
from bibtexmagic.bibtexmagic.bibtexmagic import BibTexParserOptions


class TestTitleField(unittest.TestCase):
    def setUp(self):
        self.parser_options = BibTexParserOptions(
            pages_double_hyphened=False,
            latex_to_unicode=False)

    def test_create_field(self):
        f1 = field.BibTexField.create_field(
                "pages", "1-1905", self.parser_options)

        # Tests correct type
        self.assertTrue(isinstance(f1, pages.PagesBibTexField))

    def test_parse_field(self):
        value = "1-1905"
        f = field.BibTexField.create_field(
            "pages", value, self.parser_options)

        self.assertEqual(f.name, "pages")
        self.assertEqual(f.value, value)

    def test_parse_field_unicode(self):
        pages_raw = "1-1905"
        parsed_sng = pages_raw
        parsed_dbl = pages_raw.replace("-", "--")

        # Should not parse unicode
        f = field.BibTexField.create_field(
            "pages", pages_raw, self.parser_options)

        self.assertTrue(f.value, parsed_sng)

        # Now should start parsing unicode
        self.parser_options.pages_double_hyphened = True

        f = field.BibTexField.create_field(
            "pages", pages_raw, self.parser_options)

        self.assertEqual(f.value, parsed_dbl)
