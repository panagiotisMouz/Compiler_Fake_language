import os
import sys
import random

global key, line, word,names_var
global tokens,indexer,temporary
global check,names
global name_of_assi
global numes
global varl
varl=[]
numes=0
global newtups
newtups=[]
global cp

cp=open("test.c",'w')
f = open("test.int", "w")
cp.write('#include <stdio.h>\n')
check=0
temporary=0
indexer=0
i=0

def split_to_char ( words ):
    return [char for char in words]
# the creator of the token table
def matrix():
    tokens = []
    # colNum = 0
    # t_str = ""
    f = open(sys.argv[1], 'r')
    #f = open(file, encoding="utf8")
    #f = open("test.txt", encoding="utf8")

    # ALL LINES IN ONE t_strING
    allLinesInOne = f.read()

    # print(allLinesInOne)

    # ALL LINES SEPARATED IN LIST
    lines_list = allLinesInOne.split("\n")

    # print(lines_list)

    # CIMPLE KEYWORDS
    keywords_list = {'program': 'Keyword', 'declare': 'Keyword', 'if': 'Keyword', 'else': 'Keyword', 'while': 'Keyword',
                     'switchcase': 'Keyword', 'forcase': 'Keyword', 'incase': 'Keyword', 'case': 'Keyword',
                     'default': 'Keyword', 'not': 'Keyword', 'and': 'Keyword', 'or': 'Keyword', 'function': 'Keyword',
                     'procedure': 'Keyword', 'call': 'Keyword', 'return': 'Keyword', 'in': 'Keyword',
                     'inout': 'Keyword', 'input': 'Keyword', 'print': 'Keyword'}

    # CIMPLE SYMBOLS
    symbols_list = {'(': 'Symbol', ')': 'Symbol', '{': 'Symbol', '}': 'Symbol', '[': 'Symbol', ']': 'Symbol'}

    # CIMPLE NUMBERS
    numbers_list = {'1': 'Number', '2': 'Number', '3': 'Number', '4': 'Number', '5': 'Number', '6': 'Number',
                    '7': 'Number', '8': 'Number', '9': 'Number', '0': 'Number'}

    # CIMPLE OPERATORS
    operators_list = {'+': 'addOp', '-': 'addOp', '*': 'mulOp', '/': 'mulOp', '==': 'relOp', '>=': 'relOp',
                      '<': 'relOp', '>': 'relOp', '<>': 'relOp', '<=': 'relOp'}

    # CIMPLE ASSIGNMENT
    assign_list = {':=': 'Assignment'}

    # CIMPLE KEYWORDS DELIMITERS
    delimiter_list = {',': 'Delimiter', '.': 'Delimiter', ';': 'Delimiter'}

    # ASCII
    alphabet_list = {'a': 'ID', 'b': 'ID', 'c': 'ID', 'd': 'ID', 'e': 'ID', 'f': 'ID', 'g': 'ID', 'h': 'ID', 'i': 'ID',
                     'j': 'ID', 'k': 'ID', 'l': 'ID', 'm': 'ID', 'n': 'ID', 'o': 'ID', 'p': 'ID', 'q': 'ID', 'r': 'ID',
                     's': 'ID', 't': 'ID', 'u': 'ID', 'v': 'ID', 'w': 'ID', 'x': 'ID', 'y': 'ID', 'z': 'ID', 'A': 'ID',
                     'B': 'ID', 'C': 'ID', 'D': 'ID', 'E': 'ID', 'F': 'ID', 'G': 'ID', 'H': 'ID', 'I': 'ID', 'J': 'ID',
                     'K': 'ID', 'L': 'ID', 'M': 'ID', 'N': 'ID', 'O': 'ID', 'P': 'ID', 'Q': 'ID', 'R': 'ID', 'S': 'ID',
                     'T': 'ID', 'U': 'ID', 'V': 'ID', 'W': 'ID', 'X': 'ID', 'Y': 'ID',
                     'Z': 'ID'}  # The alphabet combine in a list

    keywords = keywords_list.keys()
    symbols = symbols_list.keys()
    numbers = numbers_list.keys()
    operators = operators_list.keys()
    assignment = assign_list.keys()
    delimiters = delimiter_list.keys()
    alphabet = alphabet_list.keys()

    lineNum = 0
    # READ LINES
    for i in range(len(lines_list)):
        lineNum = lineNum + 1

        line = lines_list[i] + "\n"

        # REMOVES ALL TABS AND SPACES
        filter_object = filter(lambda x: x != "", line)
        line = list(filter_object)

        # SKIP ALL NULL LINES
        if line == []:
            continue

        # SPLIT LINE TO CHARS
        line = split_to_char(line)
        #print(line)
        t_str = ""
        next = 0
        n = ""
        a = ""
        relOp = ""
        comment = 0
        hold = ""
        # GO THROUGH ALL CHARS OF THE LINE
        for j in range(0, len(line)):
            num = str(lineNum)
            char = line[j]
            next = j + 1

            # IF CHARS IS NULL DON'T DO ANYTHING, ELSE CHECK CHAR FAMILY
            if char != ' ':
                # CHECK IF THERE IS A COMMENT TO SKIP
                if char == "#":
                    comment = comment + 1

                if comment == 0 or comment == 2:
                    # CHECK IF CHARACTER IS A LETTER
                    if char in alphabet:
                        t_str = t_str + char
                        t_str = "".join(t_str)
                        # CHECK IF CHARACTER IS A KEYWORD
                        if t_str in keywords:
                            # IF THE KEYWORD STARTS WITH "in" WE CHECK IF IS "in" KEYWORD OR ELSE IT WILL BE "input" KEYWORD
                            if t_str == "in" and line[j + 1] == "p":
                                continue
                            elif t_str == "in" and line[j + 1] == "o":
                                continue
                            # CHECK IF WE ARE AT THE END OF LINE TO PREVENT ERRORS
                            if j < len(line) - 1:
                                # CHECK FOR CORRECT KEYWORD EXAMPLE: "inputt", "forcase4" IS NOT A KEYWORD
                                if t_str in keywords and (line[next] == " " or line[next] == "\n" or line[next] not in alphabet or line[next] not in numbers):
                                    print("'" + t_str + "'" + " is a Keyword at line:" + num)
                                    tokens.append((t_str, lineNum, "Keyword"))
                                    # IF KEYWORD IS "forcase" WE EXPECT NEWLINE AFTER ELSE IS AN ERROR
                                    if t_str == "forcase" and line[j+1] != "\n":
                                        print('\x1b[0;31;40m' + 'Error after "forcase" at line:' + num + ". New line was expected" + '\x1b[0m')
                                        exit()
                                    t_str = ""
                                    hold = ""
                                    continue
                           # print("'" + t_str + "'" + " is a Keyword in line:" + num)
                           # tokens.append((t_str, lineNum, "Keyword"))
                           # t_str = ""
                           # hold = ""
                        else:
                            hold = t_str
                    # ELSE IF IS NOT A LETTER CHECK THIS:
                    elif char in numbers and line[j - 1] in alphabet:
                        hold = hold + char
                        hold = "".join(hold)
                    elif char in numbers and line[j - 1] in numbers and hold != "":
                        hold = hold + char
                        hold = "".join(hold)
                    else:
                        if (31 > len(hold) > 0) and hold not in keywords and char != "#":
                            print("'" + hold + "'" + " is an ID at line:" + num)
                            tokens.append((hold, lineNum, "ID"))
                            hold = ""
                        hold = ""
                        # t_str = ""
                        # t_str = t_str + char
                        # t_str = "".join(t_str)
                        if char in symbols:
                            print("'" + char + "'" + " is a Symbol at line:" + num)
                            tokens.append((char, lineNum, "Symbol"))
                            t_str = ""

                        if char in numbers and line[j - 1] not in alphabet:
                            n = n + char
                            n = "".join(n)
                            if j < len(line) - 1:
                                if line[j + 1] not in numbers:
                                    print("'" + n + "'" + " is a Number at line:" + num)
                                    tokens.append((n, lineNum, "Number"))
                                    n = ""
                                if line[j + 1] in alphabet:
                                    exit("Syntax Error at line:" + num + " can't write letter after number")
                            else:
                                print("'" + n + "'" + " is a Number at line:" + num)
                                tokens.append((n, lineNum, "Number"))
                                n = ""

                        if char in delimiters:
                            print("'" + char + "'" + " is a Delimiter at line:" + num)
                            tokens.append((char, lineNum, "Delimiter"))
                            t_str = ""
                            if char == "." and line[j - 1] == "}":
                                print()
                                print('\x1b[6;30;42m' + 'End of token reader. Success!' + '\x1b[0m')
                                print()


                        if char in operators or char == "=" and (j < len(line) - 1):
                            if char == "+" or char == "-":
                                print("'" + char + "'" + " is a addOp Operator at line:" + num)
                                tokens.append((char, lineNum, "addOp"))
                                t_str = ""
                            if char == "*" or char == "/":
                                print("'" + char + "'" + " is a mullOp Operator at line:" + num)
                                tokens.append((char, lineNum, "mulOp"))
                                t_str = ""
                            if char == ">" and line[j-1] == "<":
                                t_str = "<>"
                                print("'" + t_str + "'" + " is an relOp Operator at line:" + num)
                                tokens.append((t_str, lineNum, "RelOp"))
                                t_str = ""
                            elif (char == "<" or char == ">") and (line[j + 1] != "=" and line[j + 1] != ">"):
                                print("'" + char + "'" + " is a relOp Operator at line:" + num)
                                tokens.append((char, lineNum, "RelOp"))
                                t_str = ""
                            elif char == "<" and line[j+1] == ">":
                                continue
                            if line[j] == "=" and (line[j - 1] == "<" or line[j - 1] == ">"):

                                relOp = line[j - 1] + line[j]
                                relOp = "".join(relOp)
                                print("'" + relOp + "'" + " is a relOp Operator at line:" + num)
                                tokens.append((relOp, lineNum, "RelOp"))
                                relOp = ""

                            if char == "=":
                                a = a + char
                                a = "".join(a)
                                if a == "==":
                                    print("'" + a + "'" + " is a relOp Operator at line:" + num)
                                    tokens.append((a, lineNum, "RelOp"))
                                    a = ""
                                elif line[j+1] != "=" and line[j-1] != ":":
                                    print('\x1b[0;31;40m' + 'Error at line:' + num + ". ':' or '=' was expected before '=' " + '\x1b[0m')
                                    exit()
                        if char == ":":
                            if line[j + 1] == "=":
                                print("':='" + " is an Assignment at line:" + num)
                                tokens.append((":=", lineNum, "Assignment"))
                                t_str = ""
    #for t in range(len(tokens)):
     #   ft.write(str(tokens[t]))
      #  ft.write("\n")
    #ft.close()
    return tokens


# It gives you the next token
def lex():
    global indexer
    token = tokens[indexer]

    indexer += 1
    a=token
    (key,line,word)=a

    return key

# It gives you family type of the current token
def family():
    token = tokens[indexer-1]
    a = token
    (key, line, word) = a
    return word

# it gives you the current line number
def lines():
    token = tokens[indexer-1]
    a = token
    (key, line, word) = a
    return line

# it gives you the symbol that the current token is
def symbol():
    a= tokens[indexer-1]
    (key, line, word) = a
    return key

def get_token():  # Thats how i get the next token
    return lex()

# here starts the program by starting the program analysis
def syntax_analyzer():
    program()
    print('compilation successfully completed')

# here i check if the first line is correctly written
# And after that it calls the next method block
# if the whole program finishes without errors it comes back to the program method
# and checks if the final part is .
def program():
    global names
    get_token()
    if symbol()=='program':
        get_token()
        if family()=='ID':
            names=symbol()
            get_token()
            block() # i call the method block to continue
            if symbol()=='}':
                get_token()
            if symbol() == '.': # I check if the end of the program its correct
                genquad('halt', '_', '_', '_')
                genquad('end_block', names, '_', '_')
                print("Its done")
            else:
                print("Line:", lines(), "Symbol:", symbol())
                return exit("Error its the . delimiter must be the end of the line and the program")
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error you need a valid ID for the program")
    else:
        print("Line:", lines(), "Symbol:", symbol())
        return exit("Error its the beginning of the program always starts with program ID { ")

def block():
    global names
    if(symbol()=='{'):
        get_token() # for the next token in line
        declarations() # where we declare all the variables
        subprograms()  # here we check for fuctions and procudures
        if check==0:
            genquad('begin_block', names, '_', '_')
        blockstatements()  # it checks for everything else
    else:
        print("Line:", lines(), "Symbol:", symbol())
        return exit("Error after the program and the ID you need to open the block with the group symbol '{' ")

def declarations():

    while symbol()=='declare':
        get_token()
        valist() # here i check if there is ID after the declare keyword and if there are more ids involved


# here i check if there is ID after the declare keyword and if there are more ids involved
def valist():
    global varl

    if family()=='ID':
        varl.append(symbol())
        get_token()
        while symbol()==',':
            get_token()
            if family()=='ID':
                varl.append(symbol())
                get_token()
                if symbol() != ';' and symbol() != ',':
                    print("line", lines(), "Symbol:", symbol())
                    return exit("Error symbol ; or , expected ")
                if symbol()==';':
                    get_token()
            else:
                print("line", lines(), "Symbol:", symbol())
                return exit("Error symbol ID was expected ")
        if symbol() == ';':
            get_token()
        varl.append(';')

def subprograms():
    global check
    while symbol()=='function' or symbol()=='procedure':
        subprogram()

def subprogram():
    global check_fun,check
    if symbol() == 'function':
        get_token()
        check=check+1
        if family() == 'ID':
            name=symbol()
            genquad('begin_block', name, '_', '_')
            get_token()
            if symbol() == '(':
                get_token()
                if symbol() != ')':
                    formalparlist()
                if symbol() == ')':
                    get_token()
                    block()
                    if symbol()=='}':
                        get_token()
                    genquad('end_block', name, '_', '_')
                    check=check-1
                if check_fun == False:
                    print("Line:", lines(), "Symbol:", symbol())
                    return exit("Error you need a return statement in the fuction")
            else:
                print("Line:", lines(), "Symbol:", symbol())
                return exit("Error ) group symbol was expected")
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error the group symbol ( was expected")

    if symbol() == 'procedure':
        get_token()
        check = check + 1
        if family() == 'ID':
            name=symbol()
            genquad('begin_block', name, '_', '_')
            get_token()
            if symbol() == '(':
                get_token()
                if symbol()!=')':
                    formalparlist()
                if symbol() == ')':
                    get_token()
                    block()
                    if symbol()=='}':
                        get_token()
                    genquad('end_block', name, '_', '_')
                    check=check-1
            else:
                print("Line:", lines(), "Symbol:", symbol())
                return exit("Error ) group symbol was expected")
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error the group symbol ( was expected")

def formalparlist():
    formalparitem()
    while symbol()==',':
        get_token()
        formalparitem()

def formalparitem():

    if symbol()=='in':
        get_token()
        if family()=='ID':
            get_token()
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error  ID was expected")
    elif symbol()=='inout':
        get_token()
        if family()=='ID':
            get_token()
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error  ID was expected")
    else:
        print("Line:", lines(), "Symbol:", symbol())
        return exit("Error  ID was expected or an extra , was found")

def blockstatements():
    while symbol()!='}':
        statement()

def statement():

    inputStat()
    assignStat()
    ifStat()
    whileStat()
    switchcaseStat()
    forcaseStat()
    incaseStat()
    callStat()
    returnStat()
    printStat()

def inputStat():
    if symbol()=='input':
        get_token()
        if symbol()=='(':
            get_token()
            if family() =='ID':
                genquad('in', '_', '_',symbol() )
                get_token()
                if symbol()!=')':
                    print("Line:", lines(), "Symbol:", symbol())
                    return exit("Error  ) was expected")
                get_token()
                if symbol()!=';':
                    print("Line:", lines(), "Symbol:", symbol())
                    return exit("Error  ; was expected")
                get_token()
            else:
                print("Line:", lines(), "Symbol:", symbol())
                return exit("Error  ID was expected")
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error  ( was expected")

def assignStat():
    global name_of_assi
    if family()=='ID':
        name_of_assi = symbol()
        get_token()
        if symbol()==':=':
            expression()
            if symbol()!=';':
                print("Line:", lines(), "Symbol:", symbol())
                return exit("Error ; was expected for assigment")
            get_token()
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error := was expected for assigment")

def ifStat():
    if symbol()=='if':
        get_token()
        if symbol() == '(':
            condition() # i check for the conditions inside the ()
            if symbol() == ')':
                get_token()
                if symbol()=='{':
                    get_token()
                    statement()# i check for the {} if its probably closed
                    if symbol()!='}':
                        print("Line:", lines(), "Symbol:", symbol())
                        return exit("Error you need to close the groubSymbol ')' ")
                else:
                    statement()
                elsepart() # it takes to the else statement
            else:
                print("Line:", lines(), "Symbol:", symbol())
                return exit("Error you need to close the groubSymbol ')' ")
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error you need '(' group symbols after the if statement ")

def elsepart():
    if symbol() == 'else':
        get_token()
        if symbol()=='{':
            get_token()
            genquad('jumb', '_', '_', '_')
            statement()
    else:
        get_token()

def switchcaseStat():

    if symbol()=='switchcase':

        get_token()
        while symbol()=='case':

            get_token()
            if symbol() =='(':

                condition() # every condition after it finishes it has getotken to get the next one

                if symbol() !=')':
                    print("Line:", lines(), "Symbol:", symbol())
                    return exit("Error  ) was expected")
                get_token()
                statement()

            else:
                print("Line:", lines(), "Symbol:", symbol())
                return exit("Error  ( was expected")
        if symbol() == 'default':
            get_token()
            statement()

        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error case wrong look again the layout of the switch case")

def forcaseStat():


    if symbol()=='forcase':
        get_token()
        while symbol()=='case':
            get_token()
            if symbol() =='(':



                condition()

                if symbol() !=')':
                    print("Line:", lines(), "Symbol:", symbol())
                    return exit("Error  ')' was expected")
                get_token()
                statement()

            else:
                print("Line:", lines(), "Symbol:", symbol())
                return exit("Error  '(' was expected")

        if symbol() == 'default':
            get_token()
            statement()

        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error  wrong layout of the forcase case")

def incaseStat():
    global counting

    if symbol()=='incase':
        get_token()
        while symbol()=='case':
            get_token()
            if symbol()=='(':
                condition()
                if symbol()!=')':
                    print("Line:", lines(), "Symbol:", symbol())
                    return exit("Error  ) was expected")
                get_token()
                statement()

            else:
                print("Line:", lines(), "Symbol:", symbol())
                return exit("Error  ( was expected")

def whileStat():
    global counting,checking_contion,table_of_contisions
    if symbol()=='while':
        get_token()
        if symbol() =='(':
            condition()
            if symbol()==')':
                get_token()
                if symbol()=='{':
                    block()
                else:
                    statement()
            else:
                print("Line:", lines(), "Symbol:", symbol())
                return exit("Error ) was expected")
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error a  ( was expected")

def callStat():
    if symbol()=='call':
        name=get_token()
        if family()=='ID':
            get_token()
            if symbol()=='(':
                get_token()
                while symbol()!=')':
                    if symbol()=='in':
                        get_token()
                        genquad('par',symbol(),'cv','_')
                    if symbol()=='inout':
                        get_token()
                        genquad('par', symbol(), 'ref', '_')
                    get_token()
                genquad('call',name,'_','_')
                if symbol()!=')':
                    print("Line:", lines(), "Symbol:", symbol())
                    return exit("Error  ) was expected")
                get_token()
                if symbol()!=';':
                    print("Line:", lines(), "Symbol:", symbol())
                    return exit("Error  ; was expected")
                get_token()
            else:
                print("Line:", lines(), "Symbol:", symbol())
                return exit("Error  ( was expected")
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error  ID  was expected")

def returnStat():
    global check_fun
    if symbol()=='return':
        get_token()
        check_fun=True
        if symbol()=='(':
            ret()
            if symbol()==';':
                get_token()
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error  ( was expected")

def printStat():
    if symbol()=='print':
        get_token()
        if symbol()=='(':
            pri()
            if symbol() == ';':
                get_token()
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error  ( was expected")

def expression():
    global name_of_assi
    i=0
    j=0
    t=[]
    k=[]
    temps=[]
    if symbol()!='(':
        while True:
            if symbol() == '(':
                get_token()
                k.append(symbol())
                while symbol()!=')' and symbol()!=';':
                    get_token()
                    k.append(symbol())
            else:
                while symbol() !='(' and symbol()!=';':

                    get_token()
                    t.append(symbol())
                    if family()=='ID':
                        name=symbol()
                        get_token()
                        t.append(symbol())
                        if symbol()=='(':
                            while symbol() != ')':
                                if symbol() == 'in':
                                    get_token()
                                    genquad('par', symbol(), 'cv', '_')
                                if symbol() == 'inout':
                                    get_token()
                                    genquad('par', symbol(), 'ref', '_')
                                get_token()
                            genquad('call', name, '_', '_')
                            get_token()
                            t.pop()
                            t.pop()
            if symbol()==';':
                break
        while len(k)!=0:
            w = newtemp()
            te1=k.pop(0) #arithmos i id 1
            while te1!=')':
                op=k.pop(0)
                if op==')':
                    break
                if op=='mulOp' or op=='addOp':
                    j=j+1
                te2=k.pop(0)
                if j>1 :
                    genquad(op,w,te2,x)
                    temps.append(x)
                    w=x
                    x=newtemp()
                else:
                    genquad(op,te1,te2,w)
                    temps.append(w)
                    x=newtemp()
        while len(t)!=0:
            te1=t.pop(0) #arithmos i id 1
            if te1=='mulOp' or te1=='addOp':
                te1=t.pop(0)
                while te1=='mulOp' or te1=='addOp':
                    i=1
                    w=newtemp()
                    genquad(te1,temps.pop(0),temps.pop(0),w)
                if te1=='('and te1==';' and i==1:
                    genquad(':=',w,'_',name_of_assi)
                    break
                else:
                    genquad(':=', te1, '_', name_of_assi)
                    break
            if len(temps)==0 and len(t)==1:
                t.pop(0)
                genquad(':=', te1, '_', name_of_assi)
                break
            w=newtemp()
            while len(temps)==0:
                op = t.pop(0)
                if op == ';':
                    break
                if op == 'mulOp' or op == 'addOp':
                    j = j + 1
                te2 = t.pop(0)
                if j > 1:
                    genquad(op, w, te2, x)
                    w = x
                    x = newtemp()
                else:
                    genquad(op, te1, te2, w)
                    x = newtemp()
            while len(temps)!=0:
                op=t.pop(0)
                te2=t.pop(0)
                if te2=='(':
                    genquad(op,te1,temps.pop(0),w)
                    te1=w
                    w=newtemp()
                else:
                    genquad(op,te1,te2,w)
                    w=newtemp()
            genquad(':=',w,'_',name_of_assi)

def pri():
    i = 0
    while True:
        if symbol() == '(':
            i = i + 1
        get_token()
        if symbol() == ')':
            i = i - 1
        if i == 0:
            get_token()
            genquad('out', w,'_', '_')
            break
        w = symbol()

def ret():
    i=0
    while True:
        if symbol()=='(':
            i=i+1
        get_token()
        if symbol()==')':
            i=i-1
        if i==0:
            get_token()
            genquad('rev',w,'_','_')
            break
        w=symbol()


def condition():
    global newtups
    temp1=get_token()
    get_token()

    while True:
        if family()=='multOp' or family()=='addOp':
            op=symbol()
            temp2=get_token()
            w=newtemp()
            genquad(op,temp1,temp2,w)
            temp1=w
        else:
            op=symbol()
            temp2=get_token()
            get_token()

        if symbol()=='and' or symbol()=='or':
            temp1=get_token()
            op=get_token()
            temp2=get_token()
            get_token()
            if symbol() == ')':
                genquad(op, temp1, temp2, '_')
                genquad('jumb', '_', '_', '_')
                break
        elif symbol()==')':
            tem=makelist(nextquad())
            temp = makelist(currentquad())
            genquad(op,temp1,temp2,'_')


            x = nextquad()

            genquad('jumb','_','_','_')
            y = nextquad()
            backpatch(temp, x)

            backpatch(tem,y)

            break

def num():
    if symbol()=='+':
        get_token()
    elif symbol()=='-':
        get_token()
    elif symbol()=='/':
        get_token()
    elif symbol()=='*':
        get_token()

def real_OP():
    if symbol()=='=':
        get_token()
    elif symbol()=='<':
        get_token()
    elif symbol()=='<=':
        get_token()
    elif symbol()=='>':
        get_token()
    elif symbol()=='>=':
        get_token()
    elif symbol()=='<>':
        get_token()

def logi():
    if symbol()=='OR':
        get_token()
    elif symbol()=='AND':
        get_token()

def currentquad():
    global numes
    return numes

def nextquad():
    global numes
    next_num = numes + 1
    return next_num

def newtemp():
    global temporary

    T = 'T_' + str(temporary)
    temporary = temporary + 1

    return T

def emptylist():
    global empty_List
    empty_List = list()
    return empty_List

def makelist(x):
    global label_list
    label_list = list()
    label_list.append(x)

    return label_list

def merge(x,y):
    x = x + y
    return x

def backpatch(list,z):
    global newtups

    for i in newtups:
        if i[0] in list:
            i[4]=z

def genquad(op, x, y, z):
    global newtups,numes
    newtups.append(list([numes, op, x, y, z]))
    numes=numes+1

def middlec():
    global newtups,names,varl
    label = 0
    main=[]

    for r in varl:
        if r==';':
            varl.pop(0)
            break
        main.append(r)
    varl.pop(0)
    varl.pop(0)


    for i in newtups:
        if i[1]=="begin_block" and i[2]!=names:
            if i[2]=='proc':
                cp.write('int '+str(i[2])+'( int '+main[0]+' , int '+main[1]+' ){\n')
                for j in varl:
                    if j == ';':
                        varl.pop(0)
                        break
                    cp.write('int '+ j +';\n ')
                varl.pop(0)
            else:

                cp.write('int ' + str(i[2]) + '(){\n')
                for j in varl:
                    if j == ';':
                        varl.pop(0)
                        break
                    cp.write('int ' + j + ';\n ')



        if i[1]=="begin_block" and i[2]==names:
            cp.write('int '+'main'+'(){\n')
            for j in main:
                cp.write('int '+ j +';\n ')

        if i[1] == "end_block" and i[2]!=names:
            cp.write('}\n')

        if i[1] == "jumb":
            cp.write(" L_" + str(label) + ": " + "goto " + "L_" + str(label+2) + "; //("+str(i[1])+','+str(i[2])+','+str(i[3])+','+str(i[4])+")\n")
            label = label + 1
        if i[1] == "+" or i[1] == "-" or i[1] == "*" or i[1] == "/":
            cp.write(" L_" + str(label) + ": " + str(i[4]) + "=" + str(i[2]) + str(i[1]) + str(i[3]) +"; //("+str(i[1])+','+str(i[2])+','+str(i[3])+','+str(i[4])+")\n")
            label = label + 1
        if i[1] == "=" or i[1] == ">" or i[1] == "<" or i[1] == "<=" or i[1] == ">=" or i[1] == "<>":
            cp.write(
                " L_" + str(label) + ": if (" + str(i[2]) + str(i[1]) + str(i[3]) + ") goto L_" + str(label+2) + "; //("+str(i[1])+','+str(i[2])+','+str(i[3])+','+str(i[4])+")\n")
            label = label + 1
        if i[1] == ":=":
            cp.write(" L_" + str(label) + ": " + str(i[4]) + "=" + str(i[2]) + "; //("+str(i[1])+','+str(i[2])+','+str(i[3])+','+str(i[4])+")\n")
            label = label + 1
        if i[1] == "rev":
            cp.write(" L_" + str(label) + ": return " + str(i[2]) + "; //("+str(i[1])+','+str(i[2])+','+str(i[3])+','+str(i[4])+")\n")
            label = label + 1
        if i[1] == "out":
            cp.write(" L_" + str(label) + ": printf(" + '"%d"' + "," + str(i[2]) + "); //("+str(i[1])+','+str(i[2])+','+str(i[3])+','+str(i[4])+")\n")
            label = label + 1
        if i[1]== "call":
            if i[2]=='func':
                cp.write(" L_" + str(label) + ": " + str(i[2]) + "( ); //(" + str(i[1]) + ',' + str(i[2]) + ',' + str(i[3]) + ',' + str(i[4]) + ")\n")
                label = label + 1
            else:
                cp.write(" L_" + str(label) + ": "+ str(i[2])+ "("+main[0]+','+main[1]+"); //("+str(i[1])+','+str(i[2])+','+str(i[3])+','+str(i[4])+")\n")
                label=label+1
    cp.write(" L_" + str(label) + ": {}\n")
    cp.write("}")
    cp.close()

def middle():
    global newtups
    for i in range(len(newtups)):
        f.write(str(newtups[i][0]) + ': ')
        f.write(str(newtups[i][1]) + ', ')
        f.write(str(newtups[i][2]) + ', ')
        f.write(str(newtups[i][3]) + ', ')
        f.write(str(newtups[i][4]) + '\n')
    f.close()

def ran():
    n=random.randint(0,100)
    return n
# its for keeping track the $s registers every time i need it for sw or lw
def sreg():
    global sreg_num
    sreg_num+=1
    return "$t"+str(sreg_num)
# its for keeping track the $t0-8 registers every time i need it for sw or lw
def tregisters():
    global treg
    treg+=1
    if treg==8:
        treg=-1
    return "$t"+str(treg)
# its for keeping track the $a0-4 registers every time i need it for sw or lw
def areg():
    global areg_num
    areg_num+=1
    if areg_num==4:
        areg_num=0
    return "$a"+str(areg_num)
# its for keeping track the $v0-2 registers every time i need it for sw or lw
def vreg():
    global vreg_num
    vreg_num = vreg_num + 1
    if vreg_num==2:
        vreg_num=0
    return "$v"+str(vreg_num)
# its for the labels L: in the assemply format
def count():
    global counting
    counting=int(counting) + 1
    return str(counting)
def next_count():
    global counting
    t=int(counting)+1
    return str(t)
# the main goal of the scope is to follow a variable until no longer use
class Scope:
    def Scope(scopes):
        scopes.enList = [] # The main list of Entities
        scopes.listlevel=[]
        scopes.Level = 0  # level of nesting in the statements
        scopes.name ='' # The name of the current Scope
        scopes.selfclosing = None #If the Scope has closed
y=0 # To check if there command is prosedure or fuction
scopes = Scope() # Creating the items of scopes and entities ( THE REASON OF THE ERROR)
scopes.Scope()
#After the newscope you save the old entity in it
def newEntity(y): # saves the old entity in the enlist
    global scopes
    scopes.enList.append(y)

def nescopes(y): # i create a new scope item that is used to track other varebles,name and there current nesting levels
    global scopes
    x = Scope()
    x.name = y
    x.selfclosing = scopes

    if scopes == None:
        x.selfclosing = 0
    else:
        x.Level + 1

    scopes = y
# delete a scope that its finish with the nesting and its no longer in use
def delscopes():
    global scopes
    del scopes
    scopes = scopes.enList


# I check and calculate the current offset of every scope vareble
def offset():
    global scopes,offsets
    off.append(offsets)
    if len(scopes.enList) != 0:
        for i in scopes.enList:
            if i.type == 'par' or i.type == 'temp' or i.type == 'variable' : # if there is any type of vareble with that name i change the offset  +1
                offsets = offsets + 4
    offsets = (offsets + 4)

    return offsets
# i check for there is a procedure or a fuction so i can give them the offset of there length of actions
def framelength():
    global scopes,checks
    if checks==0:
        t=Entity.function()
        t.framelength=offset()
    else:
        t=Entity.procudure()
        t.framelength=offset()
# i check for there is a procedure or a fuction so i can give them the next label number which they start with
def startQuad():
    global scopes, checks
    if checks == 0:
        t = Entity.function()
        t.startQuad = nextquad()
    else:
        t = Entity.procudure()
        t.startQuad = nextquad()

class Entity:
    # an abstract class that help sychronize all the others
    global t

    def Entity(self):
        self.Variable=self.Variable()
        self.TemporaryVariable=self.TemporaryVariable()
        self.SymbolicConstant=self.SymbolicConstant()
        self.FormalParameter=self.FormalParameter()
        self.procudure=self.procudure()
        self.function=self.function()
        self.name=''
        self.type=''


    #inisialize the variables name type and offset
    class Variable:
        def Variable(self):
            self.name =''
            self.type = ''
            self.offset = 0

    # inisialize the temporary variables name type and offset
    class TemporaryVariable:
        def TemporaryVariable(self):
            self.name = ''
            self.type = ''
            self.offset = 0

    # inisialize and puts in variables that are constants
    class SymbolicConstant:
        def SymbolicConstant(self):
            self.name = ''
            self.datatype = ''
            self.value=0
    # fuctions and procudures are also inisilize here
    class procudure:
        def procudure(self):
            self.name=''
            self.startQuad=startQuad()
            self.framelength=0
            self.formalparameters= Entity.FormalParameter()

    class function:
        def function(self):
            self.name = ''
            self.datatype=''
            self.startQuad = startQuad()
            self.framelength = 0
            self.formalparameters = Entity.FormalParameter()
# this parameters are used and inisialize for use in the fuctions and procudures
    class FormalParameter:
        def FormalParameter(self):
            self.name = ''
            self.datatype = ''
            self.mode = ''
            self.offset=0

# v: source variable
# reg: target register
def loadvr(v,reg):#pernoume tin metavliti v k tin topothetoume sto register reg
    global scopes

    for i in range(len(scopes.enList)):


        t=scopes.enList[i]
        name=t.Variable
        proc=t.FormalParameter.mode
        if v==name:
            asm.write("\t li "+reg+","+str(v)+"\n")
        else:
            if name=='constant':
                asm.write("\t lw " + reg + ",-" + str(t.Variable.offset) + "($gp)" + "\n")
                break
            elif name=='cv' and scopes.listlevel[i] ==0 :
                asm.write("\t lw " + reg + ",-" + str(t.Variable.offset) +"($sp)"+ "\n")
                break
            elif proc=='ref'and scopes.listlevel[i] ==0:
                asm.write("\t lw $t0,-" + str(t.FormalParameter.offset) + "($sp)\n")
                asm.write("\t lw " + reg + ",($t0)\n")
                break
            elif name == 'cv' and scopes.listlevel[i] != 0:
                gnlvcode(t.Variable.name)
                asm.write("\t lw " + reg + ",($t0)\n")
                break
            elif proc == 'ref' and scopes.listlevel[i] != 0:
                gnlvcode(t.Variable.name)
                asm.write("\t lw $t0,($t0)\n")
                asm.write("\t lw" + reg + ",($t0)\n")
                break

def storevr(reg,v): # pernoume ton register k vlepoume tin metavliti opou einai kataxorimeni se afto
    global scopes

    for i in range(len(scopes.enList)):
        t = scopes.enList[i]
        name = t.Variable.type
        proc = t.FormalParameter.mode
        if v == name:
            asm.write("\t li " + reg + "," + str(v) + "\n")
        else:
            if name == 'constant':
                loadvr(v,reg)
                storevr(reg,v)
                break
            elif name == 'cv' and scopes.listlevel[i] == 0:
                asm.write("\t sw " + reg + ",-" + str(t.Variable.offset) + "($sp)" + "\n")
                break
            elif proc == 'ref' and scopes.listlevel[i] == 0:
                asm.write("\t lw $t0,-" + str(t.FormalParameter.offset) + "($sp)\n")
                asm.write("\t sw " + reg + ",($t0)\n")
                break
            elif name == 'cv' and scopes.listlevel[i] != 0:
                gnlvcode(t.Variable.name)
                asm.write("\t sw " + reg + ",($t0)\n")
                break
            elif proc == 'ref' and scopes.listlevel[i] != 0:
                gnlvcode(t.Variable.name)
                asm.write("\t lw $t0,($t0)\n")
                asm.write("\t sw" + reg + ",($t0)\n")
                asm.write("\t sw" + reg + ",($t0)\n")
                break

# its use na prospelasis metavlites i diefthinsisi gia tin metepita xrisi stin assemlpy
# v metavliti pou theli prospelasi
def gnlvcode(v):
    global scopes,t
    # i start my loading space
    asm.write("\t lw mv $t0,-8($sp)\n")
    # A for with all the variables
    for i in range(len(scopes.enList)):
        t = scopes.enList[i]
        # i put t as entity to find the name of the varieble
        t=t.Variable.name
        if v==t:
            while scopes.Level != scopes.listlevel[i]:
                asm.write("\t lw mv $t0,-8($t0)\n")
                scopes.Level=scopes.enList - 1
        asm.write("\t addi $t0,$t0,-"+str(t.Variable.offset)+"\n")
    print('Error Name of variable not found')


if __name__ == '__main__':

    tokens=matrix()
    syntax_analyzer()
    middle()
    middlec()
