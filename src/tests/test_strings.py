import pytest
from koolkit.strings import convert_case, convert_to_single_line

# ------------------------------------------------------------------------------------------------
# TEST CONVERT_TO_SINGLE_LINE()
# ------------------------------------------------------------------------------------------------

@pytest.mark.parametrize("input, expected", [
    ("Hello\nWorld", "Hello World"),
    ("Line1\nLine2\nLine3", "Line1 Line2 Line3"),
    ("   Leading and   trailing \n whitespace\t\n", "Leading and trailing whitespace"),
    ("Single line already", "Single line already"),
    ("Multiple\t\tspaces\nand tabs", "Multiple spaces and tabs"),
    ("", ""),
    ("\n\n\n", ""),
])
def test_convert_to_single_line(input, expected):
    output = convert_to_single_line(input)
    assert output == expected


# ------------------------------------------------------------------------------------------------
# TEST CONVERT_CASE()
# ------------------------------------------------------------------------------------------------

@pytest.mark.parametrize("input, to_case, expected", [
    # Title Case
    ("hello world example", "title", "Hello World Example"),
    ("hello world example", "Title Case", "Hello World Example"),

    # Sentence case
    ("hello world example", "sentence", "Hello world example"),
    ("hello world example", "Sentence case", "Hello world example"),

    # UPPER CASE
    ("hello world example", "upper", "HELLO WORLD EXAMPLE"),
    ("hello world example", "UPPER CASE", "HELLO WORLD EXAMPLE"),

    # lower case
    ("HELLO WORLD EXAMPLE", "lower", "hello world example"),
    ("HELLO WORLD EXAMPLE", "lower case", "hello world example"),

    # snake_case
    ("hello world example", "snake", "hello_world_example"),
    ("HELLO-WORLD_example", "snake_case", "hello_world_example"),

    # UPPER_SNAKE_CASE
    ("hello world example", "UPPER_SNAKE_CASE", "HELLO_WORLD_EXAMPLE"),

    # camelCase
    ("hello world example", "camel", "helloWorldExample"),
    ("HELLO-WORLD example", "camelCase", "helloWorldExample"),

    # PascalCase
    ("hello world example", "pascal", "HelloWorldExample"),
    ("HELLO_WORLD-example", "PascalCase", "HelloWorldExample"),

    # kebab-case
    ("hello world example", "kebab", "hello-world-example"),
    ("HELLO_world-EXAMPLE", "kebab-case", "hello-world-example"),
])
def test_convert_case_variants(input, to_case, expected):
    output = convert_case(text=input, to_case=to_case)
    assert  output == expected


def test_convert_case_empty_string():
    input = ''
    expected = ''
    assert convert_case(text=input, to_case="title") == expected
    assert convert_case(text=input, to_case="sentence") == expected
    assert convert_case(text=input, to_case="camel") == expected
    assert convert_case(text=input, to_case="PascalCase") == expected
    assert convert_case(text=input, to_case="snake") == expected
    assert convert_case(text=input, to_case="UPPER_SNAKE_CASE") == expected
    assert convert_case(text=input, to_case="kebab") == expected


def test_convert_case_invalid_case_style():
    with pytest.raises(ValueError):
        output = convert_case(text="example", to_case="not-a-real-style")


def test_convert_case_non_string_input():
    with pytest.raises(TypeError):
        not_a_str = 123
        output = convert_case(text=not_a_str, to_case="title")  # type: ignore
