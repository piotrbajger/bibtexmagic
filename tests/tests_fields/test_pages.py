import unittest

from bibtexmagic.bibtexmagic.fields import pages, field


class TestTitleField(unittest.TestCase):
    def test_create_field(self):
        f1 = field.BibTexField.create_field(
                "pages", "1-1905")

        # Tests correct type
        self.assertTrue(isinstance(f1, pages.PagesBibTexField))

    def test_parse_field(self):
        value = "1-1905"
        f = field.BibTexField.create_field(
            "pages", value)

        self.assertEqual(f.name, "pages")
        self.assertEqual(f.value, value)

    def test_parse_field(self):
        pages_raw = "1-1905"
        parsed_dbl = pages_raw.replace("-", "--")

        # Should not parse unicode
        f = field.BibTexField.create_field(
            "pages", pages_raw)

        self.assertTrue(f.value, parsed_dbl)