import re


def convert_to_single_line(text: str) -> str:
    """
    Create a single-line string from a multiline string by converting newlines
    (and other whitespace) to spaces.

    Args:
        text (str): The input multiline string.

    Returns:
        str: The resulting single-line string with whitespace normalized to spaces.
    """
    return re.sub(r"\s+", " ", text).strip()




def convert_case(text: str, to_case: str) -> str:
    """
    Convert a string to a specified case style.

    Supported case styles:
        - 'title' or 'Title Case'             → Title Case (each word capitalized)
        - 'sentence' or 'Sentence case'       → Sentence case (first word capitalized)
        - 'upper' or 'UPPER CASE'             → All uppercase
        - 'lower' or 'lower case'             → All lowercase
        - 'snake' or 'snake_case'             → lowercase_words_separated_by_underscores
        - 'UPPER_SNAKE_CASE'                  → UPPERCASE_WORDS_SEPARATED_BY_UNDERSCORES
        - 'camel' or 'camelCase'              → camelCase (first word lowercase, rest capitalized)
        - 'pascal' or 'PascalCase'            → PascalCase (each word capitalized, no separators)
        - 'kebab' or 'kebab-case'             → lowercase-words-separated-by-hyphens

    Args:
        text (str): The input string to convert.
        to_case (str): The desired case style. Defaults to 'sentence'.

    Returns:
        str: The text converted to the specified case style.

    Raises:
        TypeError: If 'text' is not a string.
        ValueError: If an unsupported case style is specified.
    """
    
    def split_words_from_text(text: str) -> list[str]:
        # Replace underscores and hyphens with space, then split on non-alphanumerics
        text = re.sub(r'[_\-]', ' ', text)
        return re.findall(r'[A-Za-z0-9]+', text)

    if not isinstance(text, str):
        raise TypeError(f"text must be a string, not {type(text).__name__}")

    words = split_words_from_text(text)

    match to_case:
        case "Title Case" | "title":
            return " ".join(word.capitalize() for word in words)

        case "Sentence case" | "sentence":
            if not words:
                return ""
            first_word = words[0].capitalize()
            remaining_words = " ".join(word.lower() for word in words[1:])
            return f"{first_word} {remaining_words}".strip()

        case "UPPER CASE" | "upper":
            return text.upper()

        case "lower case" | "lower":
            return text.lower()

        case "snake_case" | "snake":
            return "_".join(word.lower() for word in words)

        case "UPPER_SNAKE_CASE":
            return "_".join(word.upper() for word in words)

        case "camelCase" | "camel":
            if not words:
                return ""
            first_word = words[0].lower()
            capitalized_words = "".join(word.capitalize() for word in words[1:])
            return first_word + capitalized_words

        case "PascalCase" | "pascal":
            return "".join(word.capitalize() for word in words)

        case "kebab-case" | "kebab":
            return "-".join(word.lower() for word in words)

        case _:
            raise ValueError(f"Unknown case style: {to_case}")





def camel2under(camel_string):
    """Converts a camelcased string to underscores. Useful for turning a
    class name into a function name.

    >>> camel2under('BasicParseTest')
    'basic_parse_test'
    """
    return _camel2under_re.sub(r'_\1', camel_string).lower()


def under2camel(under_string):
    """Converts an underscored string to camelcased. Useful for turning a
    function name into a class name.

    >>> under2camel('complex_tokenizer')
    'ComplexTokenizer'
    """
    return ''.join(w.capitalize() or '_' for w in under_string.split('_'))
