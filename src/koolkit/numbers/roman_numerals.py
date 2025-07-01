from enum import Enum
from dataclasses import dataclass
from typing import Union


# The maximum number encodable using traditional Roman numerals is 3999 (MMMCMXCIX)
# The 'overline' method exists for bigger numbers, but that is not implemented here.
MAX_NUMBER = 3999


class Roman(Enum):
    """
    Enum for traditional Roman numerals.
    Expressed as uppercase, but handles lowercase > uppercase conversion via from_char() method.
    """
    I = 1
    V = 5
    X = 10
    L = 50
    C = 100
    D = 500
    M = 1000

    @classmethod
    def from_char(cls, char: str) -> 'Roman':
        try:
            return cls[char.upper()]
        except KeyError:
            raise ValueError(f'Invalid Roman numeral character: "{char}"')

    @classmethod
    def ordered(cls):
        return sorted(cls, key=lambda r: r.value, reverse=True)

    @classmethod
    def symbol_value_pairs(cls):
        return [(r.name.lower(), r.value) for r in cls.ordered()]




def convert_roman_to_arabic(roman_str: str) -> int:
    """
    Convert a Roman numeral (str) to an Arabic numeral (int).
    """

    roman_str = roman_str.strip().upper()

    if roman_str == 'N':
        return 0

    arabic_int = 0
    prev_value = 0
    repeat_count = 1

    for current_char, next_char in zip(roman_str, roman_str[1:] + ' '):
        current_value = Roman.from_char(current_char).value
        next_value = Roman.from_char(next_char).value if next_char.strip() else 0

        if current_char == next_char:
            repeat_count += 1
            if repeat_count > 3:
                raise ValueError(f'More than 3 repetitions of "{current_char}" in a row in "{roman_str}"')
        else:
            repeat_count = 1

        arabic_int += current_value if current_value >= next_value else -current_value

    return arabic_int


def convert_arabic_to_roman(arabic_int: int, lowercase: bool = False, nulla: bool = True) -> str:
    """
    Convert an Arabic numeral (int) to Roman numeral (str).
    :param arabic_int: Integer representation of the Arabic numeral that should be converted.
    :param lowercase: Boolean flag specifying whether should use lowercase letters. Default is False.
    :param nulla: Boolean flag whether an Arabic zero (0) should be returned as 'N' for nulla. Default is True. If False, then '0' will be returned.
    :return: String representation of the Roman numeral.
    """
    if arabic_int > MAX_NUMBER:
        raise ValueError(f"Cannot generate Roman numeral for {arabic_int}: exceeds {MAX_NUMBER}")

    if arabic_int == 0:
        if not nulla:
            return '0'
        else:
            return 'N' if not lowercase else 'n'

    result = []
    remainder = arabic_int
    symbols = Roman.symbol_value_pairs()

    for i, (symbol, value) in enumerate(symbols):
        while remainder >= value:
            result.append(symbol)
            remainder -= value

        # Handle subtractive notation
        offset = 2 if str(value).startswith('1') else 1 if str(value).startswith('5') else None
        if offset and i + offset < len(symbols):
            sub_symbol, sub_value = symbols[i + offset]
            if remainder >= (value - sub_value):
                result.append(sub_symbol + symbol)
                remainder -= (value - sub_value)

    roman_str = ''.join(result)
    roman_str = roman_str.upper() if not lowercase else roman_str.lower()
    return roman_str



@dataclass(frozen=True)
class RomanNumeral:
    """
    A class for Roman numerals that can handle conversion via int().
    """
    int_val: int
    str_val: str

    def __init__(self, value: Union[int, str, 'RomanNumeral'], lowercase: bool = False, nulla: bool = True):
        if isinstance(value, RomanNumeral):
            object.__setattr__(self, 'int_val', value.int_val)
            object.__setattr__(self, 'str_val', value.str_val)
        elif isinstance(value, int):
            object.__setattr__(self, 'int_val', value)
            object.__setattr__(self, 'str_val', convert_arabic_to_roman(value, lowercase=lowercase, nulla=nulla))
        elif isinstance(value, str):
            parsed = convert_roman_to_arabic(value)
            object.__setattr__(self, 'int_val', parsed)
            object.__setattr__(self, 'str_val', convert_arabic_to_roman(parsed, lowercase=lowercase))
        else:
            raise TypeError("Value must be int (Arabic number), str (Roman numeral), or RomanNumeral object.")

    def __str__(self):
        return self.str_val

    def __repr__(self):
        return self.str_val

    def __int__(self):
        return self.int_val



