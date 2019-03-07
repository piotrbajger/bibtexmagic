import re


class LatexToUni():
    """
    Responsible for converting from LaTeX macros to unicode characters
    and back. It is used to implement diacritic characters in names,
    greek letters in paper titles, etc.

    """
    def __init__(self):
        """Initialises the LatexToUni class.

        Based on the _UNI2LAT dictionary, constructs a dictionary
        with keys and values reversed to allow parsing in both
        directions.

        Static members:
            _UNI2LAT (list): A list containing pairs of the form
                [latex_macro, corresponding_regex].

        """
        unis = [pair[0] for pair in self._UNI2LAT]
        macros = [pair[1] for pair in self._UNI2LAT]
        self.pattern_uni2lat = re.compile(r'|'.join(unis))
        self.pattern_lat2uni = re.compile(r'|'.join(macros))

        # Construct dictionaries for fast lookup
        self.uni2lat_dict = {pair[0]: pair[1] for pair in self._UNI2LAT}
        self.lat2uni_dict = {pair[1]: pair[0] for pair in self._UNI2LAT}

    def uni_to_lat(self, s):
        """Replaces unicode characters with LaTeX macros.

        Args:
            s (str): String to be parsed.

        Returns:
            str: Parsed string.

        """
        return self._re_to_string(self.pattern_uni2lat.sub(
                             lambda x: self.uni2lat_dict[x.group()], s))

    def lat_to_uni(self, s):
        """Replaces LaTeX macros with their unicode equivalents
        Args:
            s (str): String to be parsed.

        Returns:
            str: Parsed string.

        """
        return self.pattern_lat2uni.sub(
                    lambda x: self.lat2uni_dict[self._string_to_re(x.group())],
                    s)

    def _string_to_re(self, s):
        """
        Convertrs from a Python string representation to
        a corresponding regex
        """
        return s.replace('\\', '\\\\').replace('^', '\\^')

    def _re_to_string(self, s):
        """Converts a regex to a corresponding Python string"""
        return s.replace('\\^', '^').replace('\\\\', '\\')

    # Source: https://gist.github.com/beniwohli/798549
    # This matches LaTeX macros with their corresponding regular expressions.
    # Note that the order of macros matters: if macro A contains macro B,
    # it has to appear _before_ it in a list, e.g. \\\\iota appears
    # before \\\\i.
    _UNI2LAT = [
                [u"\u03B9", "\\\\iota"],
                [u"\u03BB", "\\\\lambda"],
                [u"\u039B", "\\\\Lambda"],
                [u"\u00EC", "\\\\`{\\\\i}"],
                [u"\u00ED", "\\\\'{\\\\i}"],
                [u"\u00EE", "\\\\\\^{\\\\i}"],
                [u"\u00EF", "\\\\\"{\\\\i}"],
                [u"\u0129", "\\\\~{\\\\i}"],
                [u"\u012B", "\\\\={\\\\i}"],
                [u"\u012D", "\\\\u{\\\\i}"],
                [u"\u0152", "\\\\OE"],
                [u"\u0153", "\\\\oe"],
                [u"\u03A9", "\\\\Omega"],
                [u"\u03C9", "\\\\omega"],
                [u"\u00AD", "\\\\-"],
                [u"\u00B1", "\\\\pm"],
                [u"\u00B2", "{\\^2}"],
                [u"\u00B3", "{\\^3}"],
                [u"\u00B9", "{\\^1}"],
                [u"\u00C0", "\\\\`{A}"],
                [u"\u00C1", "\\\\'{A}"],
                [u"\u00C2", "\\\\{\\^}{A}"],
                [u"\u00C3", "\\\\~{A}"],
                [u"\u00C4", "\\\\\"{A}"],
                [u"\u00C5", "\\\\AA"],
                [u"\u00C6", "\\\\AE"],
                [u"\u00C7", "\\\\c{C}"],
                [u"\u00C8", "\\\\`{E}"],
                [u"\u00C9", "\\\\'{E}"],
                [u"\u00CA", "\\\\\\^{E}"],
                [u"\u00CB", "\\\\\"{E}"],
                [u"\u00CC", "\\\\`{I}"],
                [u"\u00CD", "\\\\'{I}"],
                [u"\u00CE", "\\\\\\^{I}"],
                [u"\u00CF", "\\\\\"{I}"],
                [u"\u00D0", "\\\\DH"],
                [u"\u00D1", "\\\\~{N}"],
                [u"\u00D2", "\\\\`{O}"],
                [u"\u00D3", "\\\\'{O}"],
                [u"\u00D4", "\\\\\\^{O}"],
                [u"\u00D5", "\\\\~{O}"],
                [u"\u00D6", "\\\\\"{O}"],
                [u"\u00D7", "\\\\texttimes"],
                [u"\u00D8", "\\\\O"],
                [u"\u00D9", "\\\\`{U}"],
                [u"\u00DA", "\\\\'{U}"],
                [u"\u00DB", "\\\\\\^{U}"],
                [u"\u00DC", "\\\\\"{U}"],
                [u"\u00DD", "\\\\'{Y}"],
                [u"\u00DE", "\\\\TH"],
                [u"\u00DF", "\\\\ss"],
                [u"\u00E0", "\\\\`{a}"],
                [u"\u00E1", "\\\\'{a}"],
                [u"\u00E2", "\\\\\\^{a}"],
                [u"\u00E3", "\\\\~{a}"],
                [u"\u00E4", "\\\\\"{a}"],
                [u"\u00E5", "\\\\aa"],
                [u"\u00E6", "\\\\ae"],
                [u"\u00E7", "\\\\c{c}"],
                [u"\u00E8", "\\\\`{e}"],
                [u"\u00E9", "\\\\'{e}"],
                [u"\u00EA", "\\\\\\^{e}"],
                [u"\u00EB", "\\\\\"{e}"],
                [u"\u00F0", "\\\\dh"],
                [u"\u00F1", "\\\\~{n}"],
                [u"\u00F2", "\\\\`{o}"],
                [u"\u00F3", "\\\\'{o}"],
                [u"\u00F4", "\\\\\\^{o}"],
                [u"\u00F5", "\\\\~{o}"],
                [u"\u00F6", "\\\\\"{o}"],
                [u"\u00F7", "\\\\div"],
                [u"\u00F8", "\\\\o"],
                [u"\u00F9", "\\\\`{u}"],
                [u"\u00FA", "\\\\'{u}"],
                [u"\u00FB", "\\\\\\^{u}"],
                [u"\u00FC", "\\\\\"{u}"],
                [u"\u00FD", "\\\\'{y}"],
                [u"\u00FE", "\\\\th"],
                [u"\u00FF", "\\\\\"{y}"],
                [u"\u0100", "\\\\={A}"],
                [u"\u0101", "\\\\={a}"],
                [u"\u0102", "\\\\u{A}"],
                [u"\u0103", "\\\\u{a}"],
                [u"\u0104", "\\\\k{A}"],
                [u"\u0105", "\\\\k{a}"],
                [u"\u0106", "\\\\'{C}"],
                [u"\u0107", "\\\\'{c}"],
                [u"\u0108", "\\\\\\^{C}"],
                [u"\u0109", "\\\\\\^{c}"],
                [u"\u010A", "\\\\.{C}"],
                [u"\u010B", "\\\\.{c}"],
                [u"\u010C", "\\\\v{C}"],
                [u"\u010D", "\\\\v{c}"],
                [u"\u010E", "\\\\v{D}"],
                [u"\u010F", "\\\\v{d}"],
                [u"\u0110", "\\\\DJ"],
                [u"\u0111", "\\\\dj"],
                [u"\u0112", "\\\\={E}"],
                [u"\u0113", "\\\\={e}"],
                [u"\u0114", "\\\\u{E}"],
                [u"\u0115", "\\\\u{e}"],
                [u"\u0116", "\\\\.{E}"],
                [u"\u0117", "\\\\.{e}"],
                [u"\u0118", "\\\\k{E}"],
                [u"\u0119", "\\\\k{e}"],
                [u"\u011A", "\\\\v{E}"],
                [u"\u011B", "\\\\v{e}"],
                [u"\u011C", "\\\\\\^{G}"],
                [u"\u011D", "\\\\\\^{g}"],
                [u"\u011E", "\\\\u{G}"],
                [u"\u011F", "\\\\u{g}"],
                [u"\u0120", "\\\\.{G}"],
                [u"\u0121", "\\\\.{g}"],
                [u"\u0122", "\\\\c{G}"],
                [u"\u0123", "\\\\c{g}"],
                [u"\u0124", "\\\\\\^{H}"],
                [u"\u0125", "\\\\\\^{h}"],
                [u"\u0127", "\\\\Elzxh"],
                [u"\u0128", "\\\\~{I}"],
                [u"\u012A", "\\\\={I}"],
                [u"\u012C", "\\\\u{I}"],
                [u"\u012E", "\\\\k{I}"],
                [u"\u012F", "\\\\k{i}"],
                [u"\u0130", "\\\\.{I}"],
                [u"\u0131", "\\\\i"],
                [u"\u0134", "\\\\\\^{J}"],
                [u"\u0135", "\\\\\\^{\\\\j}"],
                [u"\u0136", "\\\\c{K}"],
                [u"\u0137", "\\\\c{k}"],
                [u"\u0139", "\\\\'{L}"],
                [u"\u013A", "\\\\'{l}"],
                [u"\u013B", "\\\\c{L}"],
                [u"\u013C", "\\\\c{l}"],
                [u"\u013D", "\\\\v{L}"],
                [u"\u013E", "\\\\v{l}"],
                [u"\u0141", "\\\\L"],
                [u"\u0142", "\\\\l"],
                [u"\u0143", "\\\\'{N}"],
                [u"\u0144", "\\\\'{n}"],
                [u"\u0145", "\\\\c{N}"],
                [u"\u0146", "\\\\c{n}"],
                [u"\u0147", "\\\\v{N}"],
                [u"\u0148", "\\\\v{n}"],
                [u"\u014A", "\\\\NG"],
                [u"\u014B", "\\\\ng"],
                [u"\u014C", "\\\\={O}"],
                [u"\u014D", "\\\\={o}"],
                [u"\u014E", "\\\\u{O}"],
                [u"\u014F", "\\\\u{o}"],
                [u"\u0150", "\\\\H{O}"],
                [u"\u0151", "\\\\H{o}"],
                [u"\u0154", "\\\\'{R}"],
                [u"\u0155", "\\\\'{r}"],
                [u"\u0156", "\\\\c{R}"],
                [u"\u0157", "\\\\c{r}"],
                [u"\u0158", "\\\\v{R}"],
                [u"\u0159", "\\\\v{r}"],
                [u"\u015A", "\\\\'{S}"],
                [u"\u015B", "\\\\'{s}"],
                [u"\u015C", "\\\\\\^{S}"],
                [u"\u015D", "\\\\\\^{s}"],
                [u"\u015E", "\\\\c{S}"],
                [u"\u015F", "\\\\c{s}"],
                [u"\u0160", "\\\\v{S}"],
                [u"\u0161", "\\\\v{s}"],
                [u"\u0162", "\\\\c{T}"],
                [u"\u0163", "\\\\c{t}"],
                [u"\u0164", "\\\\v{T}"],
                [u"\u0165", "\\\\v{t}"],
                [u"\u0168", "\\\\~{U}"],
                [u"\u0169", "\\\\~{u}"],
                [u"\u016A", "\\\\={U}"],
                [u"\u016B", "\\\\={u}"],
                [u"\u016C", "\\\\u{U}"],
                [u"\u016D", "\\\\u{u}"],
                [u"\u016E", "\\\\r{U}"],
                [u"\u016F", "\\\\r{u}"],
                [u"\u0170", "\\\\H{U}"],
                [u"\u0171", "\\\\H{u}"],
                [u"\u0172", "\\\\k{U}"],
                [u"\u0173", "\\\\k{u}"],
                [u"\u0174", "\\\\\\^{W}"],
                [u"\u0175", "\\\\\\^{w}"],
                [u"\u0176", "\\\\\\^{Y}"],
                [u"\u0177", "\\\\\\^{y}"],
                [u"\u0178", "\\\\\"{Y}"],
                [u"\u0179", "\\\\'{Z}"],
                [u"\u017A", "\\\\'{z}"],
                [u"\u017B", "\\\\.{Z}"],
                [u"\u017C", "\\\\.{z}"],
                [u"\u017D", "\\\\v{Z}"],
                [u"\u017E", "\\\\v{z}"],
                [u"\u0391", "\\\\Alpha"],
                [u"\u0392", "\\\\Beta"],
                [u"\u0393", "\\\\Gamma"],
                [u"\u0394", "\\\\Delta"],
                [u"\u0395", "\\\\Epsilon"],
                [u"\u0396", "\\\\Zeta"],
                [u"\u0397", "\\\\Eta"],
                [u"\u0398", "\\\\Theta"],
                [u"\u0399", "\\\\Iota"],
                [u"\u039A", "\\\\Kappa"],
                [u"\u039E", "\\\\Xi"],
                [u"\u03A0", "\\\\Pi"],
                [u"\u03A1", "\\\\Rho"],
                [u"\u03A3", "\\\\Sigma"],
                [u"\u03A4", "\\\\Tau"],
                [u"\u03A5", "\\\\upsilon"],
                [u"\u03A6", "\\\\Phi"],
                [u"\u03A7", "\\\\Chi"],
                [u"\u03A8", "\\\\Psi"],
                [u"\u03B1", "\\\\alpha"],
                [u"\u03B2", "\\\\beta"],
                [u"\u03B3", "\\\\gamma"],
                [u"\u03B4", "\\\\delta"],
                [u"\u03B5", "\\\\epsilon"],
                [u"\u03B6", "\\\\zeta"],
                [u"\u03B7", "\\\\eta"],
                [u"\u03B8", "\\\\texttheta"],
                [u"\u03BA", "\\\\kappa"],
                [u"\u03BC", "\\\\mu"],
                [u"\u03BD", "\\\\nu"],
                [u"\u03BE", "\\\\xi"],
                [u"\u03C0", "\\\\pi"],
                [u"\u03C1", "\\\\rho"],
                [u"\u03C2", "\\\\varsigma"],
                [u"\u03C3", "\\\\sigma"],
                [u"\u03C4", "\\\\tau"],
                [u"\u03C5", "\\\\Upsilon"],
                [u"\u03C6", "\\\\varphi"],
                [u"\u03C7", "\\\\chi"],
                [u"\u03C8", "\\\\psi"],
        ]
