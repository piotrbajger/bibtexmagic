import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from bibtexmagic.bibtexmagic.latextouni import LatexToUni

class LatexToUnicodeTest(unittest.TestCase):
    def test_latex_to_uni(self):
        converter = LatexToUni()

        for uni, lat in converter._UNI2LAT.items():
            #The two replaces below allow to go back and forth between
            #usual string escaping and escapes necessary for the regex
            #to work
            lat = lat.replace('\\^', '^').replace('\\\\', '\\')
            self.assertTrue(uni == converter.lat_to_uni(lat))

    def test_uni_to_latex(self):
        converter = LatexToUni()

        for uni, lat in converter._UNI2LAT.items():
            self.assertTrue(lat == converter.uni_to_lat(uni))
