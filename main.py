import os, sys, re, tokenize, keyword, io
from method import Method

builtins = [
    'ArithmeticError','AssertionError','AttributeError','BaseException','BufferError','BytesWarning','DeprecationWarning','EOFError','Ellipsis','EnvironmentError','Exception','False','FloatingPointError','FutureWarning','GeneratorExit','IOError','ImportError','ImportWarning','IndentationError','IndexError','KeyError','KeyboardInterrupt','LookupError','MemoryError','NameError','None','NotImplemented','NotImplementedError','OSError','OverflowError','PendingDeprecationWarning','ReferenceError','RuntimeError','RuntimeWarning',
    'StandardError','StopIteration','SyntaxError','SyntaxWarning','SystemError','SystemExit','TabError','True','TypeError','UnboundLocalError','UnicodeDecodeError','UnicodeEncodeError','UnicodeError','UnicodeTranslateError','UnicodeWarning','UserWarning','ValueError','Warning','ZeroDivisionError','__IPYTHON__','__IPYTHON__active','__debug__','__doc__','__import__','__name__','__package__','abs','all','any','apply','basestring','bin','bool','buffer','bytearray','bytes','callable','chr','classmethod','cmp','coerce','compile','complex','copyright',
    'credits','delattr','dict','dir','divmod','dreload','enumerate','eval','execfile','exit','file','filter','float','format','frozenset','getattr','globals','hasattr','hash','help','hex','id','input','int','intern','ip_set_hook','ipalias','ipmagic','ipsystem','isinstance','issubclass','iter','jobs','len','license','list','locals','long',
    'map','max','min','next','object','oct','open','ord','pow','print','property','quit','range','raw_input','reduce','reload','repr','reversed','round','set','setattr','slice','sorted','staticmethod','str','sum','super','tuple','type','unichr','unicode','vars','xrange','zip'
]

reserved_words = keyword.kwlist + builtins

def listified_tokenizer(source):
    """Tokenizes *source* and returns the tokens as a list of lists."""
    io_obj = io.StringIO(source)
    tokens = []
    for a in tokenize.generate_tokens(io_obj.readline):
        tokens.append(list(a))
    return tokens

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

def pullTypes(tokens):
    names = []
    for next in tokens:
        if next[0] == 1:
            if next[4].replace('\n', '') not in names and "import" not in next[4]: #don't get import statements
                names.append(next[4].replace('\n', ''))
    return names

def findArgs(name):
    firstP = name.find("(")
    lastP = name.find(")")
    argsStr = name[firstP+1:lastP]
    # print("FIND ARGS", [x.strip() for x in argsStr.split(',')])

    return [x.strip() for x in argsStr.split(',')]

def makeMethods(analysis):
    objs = []
    numMethods = 0
    posMethods = []
    for j in range(0,len(analysis)): #start with something that starts w def, ends when run into other def
        if "def" in analysis[j]:
            numMethods = numMethods + 1
            posMethods.append(j)
    for i in range(0, numMethods):
        innerMethod = [] #strings of things in method
        tempName = ""
        tempArgs = []
        if(i == numMethods - 1):
            end = len(analysis)
        else:
            end = posMethods[i+1]-1
        for a in range(posMethods[i], end):
            if a == posMethods[i]:
                tempName = analysis[a][4]
                tempArgs = findArgs(tempName)
            else:
                if("def" not in analysis[a][4]):
                    innerMethod.append(analysis[a])
        organizedInnerMethod = organizeInnerMethod(innerMethod)
        objs.append(Method(tempName, tempArgs, organizedInnerMethod))
    return objs

def organizeInnerMethod(inner):
    list_of_insides = [] #list of lists of insides
    tempLine = inner[0][4]
    tks = []
    for next in inner:
        if next[4] == tempLine:
            tks.append(next[1])
        else:
            list_of_insides.append((tempLine, tks))
            tks = []
            tempLine = next[4]
    print(list_of_insides)
    return list_of_insides

def analyze(source): 
    tokens = listified_tokenizer(source)
    return tokens

def p(arr):
	for next in arr:
		print(next)

source = open("foo2.py").read()
analysis = analyze(source)
p(analysis)
print(makeMethods(analysis))

