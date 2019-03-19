import unittest

from bibtexmagic.bibtexmagic.fields import author, field


class TestTitleField(unittest.TestCase):
    def test_create_field(self):
        f1 = field.BibTexField.create_field(
                "author", "Test McFace")

        # Tests correct type
        self.assertTrue(isinstance(f1, author.AuthorBibTexField))

    def test_parse_author_name(self):
        testauth = author.AuthorBibTexField("test test")

        raw = [
            "Tom Waits",
            "McTestface, Facy Test",
            "Ulrich von Jungingen",
            "First de la Last",
            "von Last, Jr, First",
            "von Last, Jr, First1 First2"
        ]

        expected = [
            ["Waits", "", "Tom"],
            ["McTestface", "", "Facy Test"],
            ["von Jungingen", "", "Ulrich"],
            ["de la Last", "", "First"],
            ["von Last", "Jr", "First"],
            ["von Last", "Jr", "First1 First2"]
        ]

        for raw, parsed in zip(raw, expected):
            self.assertEqual(parsed, testauth._parse_author_name(raw))

    def test_parse_field_unicode(self):
        raw = "First La\\\'{s}t"
        parsed_no_uni = [["La\\\'{s}t", "", "First"]]
        parsed_uni = [["La\u015Bt", "", "First"]]

        # Should not parse unicode
        f = field.BibTexField.create_field(
            "author", raw)

        self.assertEqual(f.value, parsed_uni)

    def test_parse_field_multiple(self):
        authors = ' and '.join(['a', 'b', 'c', 'd'])

        f = author.AuthorBibTexField(authors)

        self.assertEqual(len(f.value), 4)
