def evaluate_as_f_string(input: str):
    """
    Takes a non-f-string that contains curly brace {placeholders},
    appends an 'f' to it, and then calls eval() to substitute the placeholders
    in what is now an f-string.

    e.g.,

        name = 'Bob'
        time = datetime.now()
        source_str = "Hello, {name}. It is {time}."

        f_str = evaluate_as_f_string(source_str)

        print(f_str)

    ⚠️ WARNING: This is a security risk -- do not use `eval` with untrusted input.
    The text within the curly braces is arbitrary Python code and could be exploited
    for malicious purposes. Cf. Bobby Tables, https://xkcd.com/327/
    """

    # The triple quote below allows multiline strings to be input.
    output = eval(f'f"""{input}"""')
    return output


