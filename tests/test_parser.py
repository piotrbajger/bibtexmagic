import unittest
import os
import json

from bibtexmagic.bibtexmagic.bibtexmagic import BibTexMagic


class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = BibTexMagic()
        self.fixture_file = os.path.join(
                os.path.dirname(__file__), "fixtures", "test_bib.bib")
        self.entries_count = 3

    def test_parse_bib(self):
        self.parser.parse_bib(self.fixture_file)
        self.assertEqual(len(self.parser.entries), self.entries_count)

    def test_to_bibtex(self):
        self.parser.parse_bib(self.fixture_file)

        bibtex_str = self.parser.to_bibtex()

        # Test if correct number of entries.
        self.assertEqual(len(bibtex_str.split("\n\n@")),
                         len(self.parser.entries) + 1)
