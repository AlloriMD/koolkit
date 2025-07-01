from koolkit.roman_numerals import RomanNumeral, convert_arabic_to_roman, convert_roman_to_arabic

PAIRS = [(13, 'XIII'),
         (1, 'I'),
         (2, 'II'),
         (3, 'III'),
         (4, 'IV'),
         (5, 'V'),
         (6, 'VI'),
         (7, 'VII'),
         (8, 'VIII'),
         (9, 'IX'),
         (10, 'X'),
         (11, 'XI'),
         (20, 'XX'),
         (21, 'XXI'),
         (30, 'XXX'),
         (31, 'XXXI'),
         (40, 'XL'),
         (41, 'XLI'),
         (50, 'L'),
         (51, 'LI'),
         (60, 'LX'),
         (70, 'LXX'),
         (80, 'LXXX'),
         (90, 'XC'),
         (91, 'XCI'),
         (100, 'C'),
         (110, 'CX'),
         (200, 'CC'),
         (300, 'CCC'),
         (400, 'CD'),
         (401, 'CDI'),
         (404, 'CDIV'),
         (409, 'CDIX'),
         (410, 'CDX'),
         (440, 'CDXL'),
         (450, 'CDL'),
         (460, 'CDLX'),
         (500, 'D'),
         (900, 'CM'),
         (901, 'CMI'),
         (904, 'CMIV'),
         (909, 'CMIX'),
         (910, 'CMX'),
         (1000, 'M'),
         (1001, 'MI'),
         (1004, 'MIV'),
         (1005, 'MV'),
         (1009, 'MIX'),
         (1010, 'MX'),
         (1040, 'MXL'),
         (1050, 'ML'),
         (1900, 'MCM'),
         (2000, 'MM'),
         (3000, 'MMM'),
         (1910, 'MCMX'),
         (1954, 'MCMLIV'),
         (1976, 'MCMLXXVI'),
         (1992, 'MCMXCII'),
         (2008, 'MMVIII'),
         ]

def test_roman_numeral_object_created_from_int():
    for arabic_int, roman_str in PAIRS:
        roman_numeral_object = RomanNumeral(arabic_int)
        assert str(roman_numeral_object) == roman_str

def test_roman_numeral_object_created_from_str():
    for arabic_int, roman_str in PAIRS:
        roman_numeral_object = RomanNumeral(roman_str)
        assert int(roman_numeral_object) == arabic_int

def test_roman_numeral_object_lowercase():
    roman_numeral_object = RomanNumeral(13, lowercase=True)
    assert str(roman_numeral_object) == 'xiii'

def test_roman_numeral_object_nulla():
    roman_numeral_object = RomanNumeral(0)
    assert str(roman_numeral_object) == 'N'

    roman_numeral_object = RomanNumeral(0, lowercase=True)
    assert str(roman_numeral_object) == "n"

    roman_numeral_object = RomanNumeral(0, nulla=False)
    assert str(roman_numeral_object) == "0"


def test_convert_roman_to_arabic():
    roman_str = 'XIII'
    arabic_int = 13
    assert convert_roman_to_arabic(roman_str) == arabic_int

def test_convert_roman_to_arabic():
    roman_str = 'XIII'
    arabic_int = 13
    assert convert_arabic_to_roman(arabic_int) == roman_str

