# -*- coding: utf-8 -*-

import tokenize

try:
    import cStringIO as io
except ImportError: # We're using Python 3
    import io

def untokenize(tokens):
    """
    Converts the output of tokenize.generate_tokens back into a human-readable
    string (that doesn't contain oddly-placed whitespace everywhere).
    .. note::
        Unlike :meth:`tokenize.untokenize`, this function requires the 3rd and
        4th items in each token tuple (though we can use lists *or* tuples).
    """
    out = ""
    last_lineno = -1
    last_col = 0
    for tok in tokens:
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        # The following two conditionals preserve indentation:
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col and token_string != '\n':
            out += (" " * (start_col - last_col))
        out += token_string
        last_col = end_col
        last_lineno = end_line
    return out

def listified_tokenizer(source):
    """Tokenizes *source* and returns the tokens as a list of lists."""
    io_obj = io.StringIO(source)
    return [list(a) for a in tokenize.generate_tokens(io_obj.readline)]