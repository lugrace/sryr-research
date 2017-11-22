import os, sys, re, tokenize, keyword, io

def listified_tokenizer(source):
    """Tokenizes *source* and returns the tokens as a list of lists."""
    io_obj = io.StringIO(source)
    return [list(a) for a in tokenize.generate_tokens(io_obj.readline)]

def enumerate_imports(tokens):
    """
    Iterates over *tokens* and returns a list of all imported modules.

    .. note:: This ignores imports using the 'as' and 'from' keywords.
    """
    imported_modules = []
    import_line = False
    from_import = False
    for index, tok in enumerate(tokens):
        token_type = tok[0]
        token_string = tok[1]
        if token_type == tokenize.NEWLINE:
            import_line = False
            from_import = False
        elif token_string == "import":
            import_line = True
        elif token_string == "from":
            from_import = True
        elif import_line:
            if token_type == tokenize.NAME and tokens[index+1][1] != 'as':
                if not from_import:
                    if token_string not in reserved_words:
                        if token_string not in imported_modules:
                            imported_modules.append(token_string)
    return imported_modules

def p(arr):
	for next in arr:
		print(next)

source = open("foo.py").read()
tokens = listified_tokenizer(source)
p(tokens)
