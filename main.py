import os, sys, re, tokenize, keyword, io
from method import Method
from collections import Counter
import nltk

builtins = [
    'ArithmeticError','AssertionError','AttributeError','BaseException','BufferError','BytesWarning','DeprecationWarning','EOFError','Ellipsis','EnvironmentError','Exception','False','FloatingPointError','FutureWarning','GeneratorExit','IOError','ImportError','ImportWarning','IndentationError','IndexError','KeyError','KeyboardInterrupt','LookupError','MemoryError','NameError','None','NotImplemented','NotImplementedError','OSError','OverflowError','PendingDeprecationWarning','ReferenceError','RuntimeError','RuntimeWarning',
    'StandardError','StopIteration','SyntaxError','SyntaxWarning','SystemError','SystemExit','TabError','True','TypeError','UnboundLocalError','UnicodeDecodeError','UnicodeEncodeError','UnicodeError','UnicodeTranslateError','UnicodeWarning','UserWarning','ValueError','Warning','ZeroDivisionError','__IPYTHON__','__IPYTHON__active','__debug__','__doc__','__import__','__name__','__package__','abs','all','any','apply','basestring','bin','bool','buffer','bytearray','bytes','callable','chr','classmethod','cmp','coerce','compile','complex','copyright',
    'credits','delattr','dict','dir','divmod','dreload','enumerate','eval','execfile','exit','file','filter','float','format','frozenset','getattr','globals','hasattr','hash','help','hex','id','input','int','intern','ip_set_hook','ipalias','ipmagic','ipsystem','isinstance','issubclass','iter','jobs','len','license','list','locals','long',
    'map','max','min','next','object','oct','open','ord','pow','print','property','quit','range','raw_input','reduce','reload','repr','reversed','round','set','setattr','slice','sorted','staticmethod','str','sum','super','tuple','type','unichr','unicode','vars','xrange','zip'
]

defaults = {'if': 'I check if ', 'for': 'I loop through', '==': 'equals'}
bad_stuff = [":", ")", "(", "\n", "\t"]

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
        organizedInnerMethod = organizeInnerMethod(tempName, innerMethod)
        appendMeMethod = Method(tempName, tempArgs, organizedInnerMethod)

        appendMeMethod.setMethodsCalled(findMethods(organizedInnerMethod))
        appendMeMethod.setBasicMethodsCalled(findBasicMethods(organizedInnerMethod))

        appendMeMethod.setDocs(makeDocs(appendMeMethod, tempName, tempArgs, organizedInnerMethod))

        objs.append(appendMeMethod)
    return objs

def organizeInnerMethod(tempName, inner):
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
    # print(tempName, " ", list_of_insides)
    return list_of_insides

def analyze(source): 
    tokens = listified_tokenizer(source)
    return tokens

def writeImports(analysis):
    doc = "I import the "
    imports = enumerate_imports(analysis)
    for next in imports:
        doc = doc + next + " and "
    doc = doc[0:len(doc)-5]
    doc = doc + " packages."
    return doc

def findMethods(inner):
    list_methods_called = []
    for next in inner:
        if "(" in next[0]:
            loc = next[1].index("(")
            if(next[1][loc-1] not in defaults):
                list_methods_called.append(next[1][loc-1])
    return list_methods_called

def findBasicMethods(inner):
    list_methods_called = []
    for next in inner:
        if "(" in next[0]:
            loc = next[1].index("(")
            if(next[1][loc-1] in defaults):
                list_methods_called.append(next[1][loc-1])
    return list_methods_called

def hub(source):
    allDocs = "There is no documentation available. Please contact the administrator."
    methods = makeMethods(source)
    misc_documentation.append(writeImports(source))
    if(len(methods) > 0 or len(misc_documentation) > 0):
        allDocs = ""
    for next in misc_documentation:
        allDocs = allDocs + next + "\n"
    for next in methods:
        allDocs = allDocs + next.toString() + "\n"

    #make basic strings for method names so i can get verb/noun for docs

    # return allDocs
    return "Documentation Completed"

def makeDocs(appendMeMethod, tempName, tempArgs, organizedInnerMethod):
    name_string = ""
    paran = tempName.find("(")
    s = split_uppercase(tempName[4:paran])
    sentence = "My main function is to " + s 
    if len(tempArgs) > 0 and tempArgs[0] != "":
        sentence = sentence + " and I do this by taking in "
        for next in tempArgs:
            sentence = sentence + next

    sentence = sentence + ". " + appendMeMethod.toString() + " "
    print("_________ ")
    for next in organizedInnerMethod:
        print(next)

    #turn everything into text and then analyze using nltk
    textified = textify(organizedInnerMethod)
    sentence = sentence + textified
    #nltk analysis on textified

    print(sentence)

    #use the split names to be like 'My main function is to [name] by [look at internal methods/what it calls]'

    return sentence

def countEnters(string):
    return string.count("\t")

def textify(organizedInnerMethod):
    return_me_sentence = ""
    enterCount = 0
    linePos = 0
    basicMethods = findBasicMethods(organizedInnerMethod)
    for next in basicMethods:
        return_me_sentence = return_me_sentence + defaults[next]
        for next2 in organizedInnerMethod:
            linePos = linePos + 1
            if(next2[1][1] == next):
                enterCount = enterCount + 1
                for i in range(3, len(next2[1])):
                    if(next2[1][i] not in bad_stuff):
                        return_me_sentence = return_me_sentence + next2[1][i] + " " + findRest(organizedInnerMethod, linePos)

    return return_me_sentence

def findRest(organizedInnerMethod, linePos):
    baseReturnMe = ""
    line = organizedInnerMethod[linePos][0]
    baseEnters = countEnters(line)-1
    print("base ", baseEnters)
    print("Line pos ", linePos)
    for i in range(0, len(organizedInnerMethod)):
        print("what ", countEnters(organizedInnerMethod[i][1]))
        if(i>linePos and countEnters(organizedInnerMethod[i][1]) >= baseEnters):
            tempLine = organizedInnerMethod[i][1]
            print("TEMP", tempLine)
            for next in tempLine:
                if(next not in bad_stuff):
                    baseReturnMe = baseReturnMe + next
    return baseReturnMe

def split_uppercase(str):
    x = ''
    i = 0
    for c in str:
        if i == 0: 
            x += c
        elif c.isupper() and not str[i-1].isupper():
            x += ' %s' % c
        else:
            x += c
        i += 1
    return x.strip()

def p(arr):
	for next in arr:
		print(next)

misc_documentation = []
source = open("foo2.py").read()
analysis = analyze(source)
print(hub(analysis))


