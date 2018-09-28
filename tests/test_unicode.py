import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from bibtexmagic.bibtexmagic.latextouni import LatexToUni

class LatexToUnicodeTest(unittest.TestCase):
    def test_latex_to_uni(self):
        converter = LatexToUni()

        for pair in converter._UNI2LAT:
            #The two replaces below allow to go back and forth between
            #usual string escaping and escapes necessary for the regex
            #to work
            lat  = pair[1].replace('\\^', '^').replace('\\\\', '\\')
            self.assertTrue(pair[0] == converter.lat_to_uni(lat))

    def test_uni_to_latex(self):
        converter = LatexToUni()

        for pair in converter._UNI2LAT:
            #The two replaces below allow to go back and forth between
            #usual string escaping and escapes necessary for the regex
            #to work
            lat  = pair[1].replace('\\^', '^').replace('\\\\', '\\')
            self.assertEqual(lat, converter.uni_to_lat(pair[0]))


    def test_are_inverses(self):
        converter = LatexToUni()

        #These two operations should be each others inverses
        macros = r"\.{z}\'{o}\l\'{c}\l\lambda"
        macros_uni = converter.lat_to_uni(macros)
        uni = converter.uni_to_lat(macros_uni)

        self.assertEqual(macros, uni)

