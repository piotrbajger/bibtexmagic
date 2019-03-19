import unittest

from bibtexmagic.bibtexmagic.fields import title, field


class TestTitleField(unittest.TestCase):
    def test_create_field(self):
        f1 = field.BibTexField.create_field(
                "title", "simple title")

        # Tests correct type
        self.assertTrue(isinstance(f1, title.TitleBibTexField))

    def test_parse_field(self):
        titles_raw = ["simple title", "simple {TITLE}"]
        titles = ["Simple title", "Simple TITLE"]

        for raw, parsed in zip(titles_raw, titles):
            f = field.BibTexField.create_field(
                "title", raw)

            self.assertEqual(f.name, "title")
            self.assertEqual(f.value, parsed)
