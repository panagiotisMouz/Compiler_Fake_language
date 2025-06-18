# Panagiotis Mouzouris 4561 cs04561
# Serafim Themistokleous 4555 cs04555

# THIS DOESNT WORK
    # I use this to start the symbol table but there is a problem with the offset fuction
    # Line 1037

import os
import sys
import random

global key, line, word,names_var
global counting,sreg_num,treg,areg_num,vreg_num
global check_fun,checking_contion,table_of_expression,table_of_contisions
global tokens,offsets
table_of_contisions=[]
table_of_expression=[]
checking_contion=False
asm=open("test.asm","w")
c=open("test.c","w")
counting=0
check_fun = False
meh=[]
i=0
inside=[()]
next_num=-1
numbering=[]
num=100
temporary=0
j=[]
sreg_num=-1
treg=-1
areg_num=-1
vreg_num=-1
formalist=[]
jumblist=[]
newtups=[[]]
ifch=False
checks=0
offsets=12
indexer=0
off=[]
names_var=[]
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
# used to split the words to characters
def split_to_char ( words ):
    return [char for char in words]
# the creator of the token table
def matrix():
    tokens = []
    # colNum = 0
    # t_str = ""
    #file = open(sys.argv[1], 'r')
    #f = open(file, encoding="utf8")
    f = open("test.txt", encoding="utf8")
    os.remove("tokens.txt")
    ft = open("tokens.txt", "a")


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


def convert(s):
    # initialization of string to ""
    new = ""
    # traverse in the string
    for x in s:
        new += x
        new +=" "
        # return string
    return new

# its a method that calls the lex method for the token
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
    global names,jumblist,ifch #So i can know when the name of the program
    get_token()
    if symbol()=='program':
        get_token()
        if family()=='ID':
            names=symbol()
            c.write("#include <stdio.h>\n")
            c.write("int main(){\n")
            asm.write('L0: b main\n')
            genquad('begin_block',names,'_','_') # Its the start to the intermedia code
            get_token()
            block() # i call the method block to continue
            if symbol() == '.': # I check if the end of the program its correct
                ifch=True # if this is True then it means you are at the end of the program
                backpatch(jumblist,nextquad())
                genquad('halt','_','_','_')
                genquad('end_block',names,'_','_')
                print("Its done")
                c.write('}\n')

            else:
                print("Line:", lines(), "Symbol:", symbol())
                return exit("Error its the . delimiter must be the end of the line and the program")
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error you need a valid ID for the program")
    else:
        print("Line:", lines(), "Symbol:", symbol())
        return exit("Error its the beginning of the program always starts with program ID { ")

#In the block() we check if the next symbol after the program id layout its the { and we call the rest
# of fuctions inside of the block and we make sure it comes back to closes } that group symbol
def block():

    if(symbol()=='{'):

        get_token() # for the next token in line
        declarations() # where we declare all the variables
        subprograms()  # here we check for fuctions and procudures
        blockstatements()  # it checks for everything else
        if(symbol()=='}'):
            get_token()
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error its the end of the block use '}' to close ")
    else:
        print("Line:", lines(), "Symbol:", symbol())
        return exit("Error after the program and the ID you need to open the block with the group symbol '{' ")

# i checks for an if keyword so it can enter here
# starts analyzing the laout of the if and if its correct it checks for an else
def ifStat():
    global ne,table_of_contisions

    if symbol()=='if':
        get_token()
        if symbol() == '(':
            get_token()
            condition() # i check for the conditions inside the ()
            table_of_contisions.pop()
            c.write('\tif('+convert(table_of_contisions)+'){\n') # i write for the C program
            table_of_contisions.clear() # clear the contitions table for the next one
            if symbol() == ')':
                get_token()
                if symbol()=='{':
                    statements()# i check for the {} if its probably closed
                    ne=makelist(nextquad()) # makes a list with the next label
                    genquad('jumb','_','_','_')# puts the jumb for the code
                    asm.write('L'+count()+':\n')
                else:
                    statements()
                    get_token()
                    ne = makelist(nextquad()) # the next list for the next label
                    genquad('jumb', '_', '_', '_')
                    asm.write('L' + count() + ':\n')
                c.write('\t}\n')
                elsepart() # it takes to the else statement
                backpatch(ne, nextquad()) # call it too fix the jumbs so the can go to the correct label
                asm.write("\t j " + next_count() + "\n")
            else:
                print("Line:", lines(), "Symbol:", symbol())
                return exit("Error you need to close the groubSymbol ')' ")
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error you need '(' group symbols after the if statement ")

# i go here if there is an else to the if statement
def elsepart():
    global ne
    get_token()

    if symbol() == 'else':
        c.write('\telse{\n')
        get_token()
        if symbol()=='{':
            statements()
            backpatch(ne,nextquad())
            asm.write("\t j "+next_count()+"\n")
            get_token()
        c.write('\t}\n')

### we dont care about declarations or valist for now
# i check with a while if got all the declares
def declarations():
    global  names_var
    while symbol()=='declare':
        get_token()
        c.write("\tint "+symbol()+";\n")
        names_var+=symbol()
        names_var+=" "
        valist() # here i check if there is ID after the declare keyword and if there are more ids involved

# here i check if there is ID after the declare keyword and if there are more ids involved
def valist():
    global names_var
    if family()=='ID':
        get_token()
        while symbol()==',':
            get_token()
            if family()=='ID':
                c.write("\tint " + symbol() + ";\n")
                names_var+=symbol()
                names_var+=" "
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

# with the statements i just go by every function to check which is it so i can call it the right one
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

# checks if the parameters in the in and inout are correct
def actualparitem():
    global table_of_expression

    get_token()

    if symbol()!='in' and symbol() !='inout':
        print("Line:", lines(), "Symbol:", symbol())
        return exit("Error keyword in or inout was expected")
    if symbol()=='in':
        get_token()
        genquad('par','_','cv','_')
        expression()
        table_of_expression.clear()
        asm.write("\t addi $fp,$sp,"+next_count()+"\n")
        loadvr('cv',sreg())
        asm.write("\t sw $t0,-"+next_count()+"($fp)\n")
    if symbol() == 'inout':
        get_token()
        genquad("par",'_','ref','_')
        asm.write("\t addi $fp,$sp," + next_count() + "\n")
        asm.write("\t lw $t0,-"+next_count()+"($sp)\n")
        asm.write("\t sw $t0,-" + next_count() + "($fp)\n")
        loadvr('ref', sreg())
        if family() !='ID':
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error an ID was expected")
        get_token()

# its the fuctions that checks for the , delimeter and its called again untill no more , delimeter
def actualparlist():

    actualparitem()
    while symbol()==',':
        actualparitem()

# checks if the tokens of the assignment are right
def assignStat():
    global endiamesos,name_of_assi,table_of_expression,scopes
    if family()=='ID':
        name_of_assi = symbol()
        x=Scope()
        y=Entity()
        y.Variable.offset=offset()
        y.type='variable'
        x.name=name_of_assi
        x.Level=0
        get_token()
        if symbol()==':=':
            get_token()
            expression()
            c.write("\t"+convert(table_of_expression)+'\n')
            asm.write("L"+count()+":\n")
            asm.write("\tli "+tregisters()+','+str(ran())+'\n')
            table_of_expression.clear()
            newEntity(y)
            if symbol()!=';':
                print("Line:", lines(), "Symbol:", symbol())
                return exit("Error ; was expected for assigment")
            get_token()
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error := was expected for assigment")

# checks if the call fuction of cimple its correct
def callStat():
    global scopes

    if symbol()=='call':
        get_token()
        genquad('call','_','_',symbol())
        if family()=='ID':
            get_token()
            if symbol()=='(':
                actualparlist()
                asm.write("L"+count()+":\n")
                asm.write("\t sw $sp,-4($fp)\n")
                asm.write("\t addi $sp,$sp,"+next_count()+"\n")
                asm.write("\t jal L"+next_count()+"\n")
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

# check if i have a or in my conditions. And i put them inside the list of the intermedia code for labels and jumbs
def condition():
    global w,y,jumblist,table_of_contisions
    y=0
    table_of_contisions.append(symbol())
    while symbol()!=')':

        t1=symbol()
        get_token()
        table_of_contisions.append(symbol())
        if family() == 'RelOp':
            if y==1:
                op= symbol()
                get_token()
                table_of_contisions.append(symbol())
                t2=symbol()
                x1 = makelist(nextquad())
                genquad(op,w , t2, '_')
                x2 = makelist(nextquad())
                jumblist.append(x2)
                genquad('jumb', '_', '_', '_')
                x=mergel(x1,x2)
                yt1=backpatch(x,nextquad())
                if op=='==':
                    asm.write("\t beq "+str(t1)+','+str(t2)+','+str(w)+'\n')
                elif op=='<>':
                    asm.write("\t bne " + str(t1) + ',' + str(t2) + ',' + str(w) + '\n')
                elif op=='<':
                    asm.write("\t blt " + str(t1) + ',' + str(t2) + ',' + str(w) + '\n')
                elif op == '>':
                    asm.write("\t bgt " + str(t1) + ',' + str(t2) + ',' + str(w) + '\n')
                elif op == '<=':
                    asm.write("\t ble " + str(t1) + ',' + str(t2) + ',' + str(w) + '\n')
                elif op == '>=':
                    asm.write("\t bge " + str(t1) + ',' + str(t2) + ',' + str(w) + '\n')
            else:
                op=symbol()
                get_token()
                table_of_contisions.append(symbol())
                t2=symbol()
                x1=makelist(nextquad())
                genquad(op,t1,t2,'_')
                x2=makelist(nextquad())
                jumblist.append(x2)
                genquad('jumb','_','_','_')
                x = mergel(x1, x2)
                yt2=backpatch(x, nextquad())
                if op=='==':
                    asm.write("\t beq "+str(t1)+','+str(t2)+','+next_count()+'\n')
                elif op=='<>':
                    asm.write("\t bne " + str(t1) + ',' + str(t2) + ',' + next_count() + '\n')
                elif op=='<':
                    asm.write("\t blt " + str(t1) + ',' + str(t2) + ',' + next_count() + '\n')
                elif op == '>':
                    asm.write("\t bgt " + str(t1) + ',' + str(t2) + ',' + next_count() + '\n')
                elif op == '<=':
                    asm.write("\t ble " + str(t1) + ',' + str(t2) + ',' + next_count() + '\n')
                elif op == '>=':
                    asm.write("\t bge " + str(t1) + ',' + str(t2) + ',' + next_count() + '\n')
        if symbol()=='and' or symbol()=='or' or symbol()=='not':
            get_token()
            table_of_contisions.append(symbol())

        if family()=='addOp'or family()=='mulOp':
            y = 1
            w=newtemp()
            op=symbol()
            get_token()
            table_of_contisions.append(symbol())
            t2=symbol()
            genquad(op,t1,t2,w)
            if op == '+':
                asm.write("\t add " + str(t1) + ',' + (t2) + ',' + (w) + '\n')
            elif op == '-':
                asm.write("\t sub " + str(t1) + ',' + (t2) + ',' + (w) + '\n')
            elif op == '/':
                asm.write("\t div " + str(t1) + ',' + (t2) + ',' + (w) + '\n')
            elif op == '*':
                asm.write("\t mul " + str(t1) + ',' + (t2) + ',' + (w) + '\n')


# i check all the expressions and i put them inside the table for later use
def expression():
    global name_of_assi,temporary,y,counter,table_of_expression,some
    table_of_expression.append(name_of_assi+'=')
    counter=0
    pinakas=[]
    iniside=[]
    y = 0
    while symbol()!=';':

        #check for () and give them priority over
        if symbol() == '(':
            table_of_expression.append(symbol())
            count = 1
            get_token()
            while count!=0:
                table_of_expression.append(symbol())
                # i check how many () there are to give priority over them and put the inside of them into the table iniside and i break if there is a ;
                if symbol()=='(':
                    count= count + 1
                if symbol()== ')':
                    count = count - 1
                iniside.append(symbol())

                get_token()
            iniside.pop()
            if symbol()==';':
                break

            # i check if there is a priority over the inside of () and do the equation while puting the result in a temporary variable for later use
            while len(iniside) != 0:

                if y > 1:
                    t1 = w
                    w = newtemp()
                    op = iniside.pop(0)
                    t2 = iniside.pop(0)
                    this=w
                    genquad(op, t1, t2, w)
                else:
                    y=y+1
                    t1 = iniside.pop(0)
                    w = newtemp()
                    op = iniside.pop(0)
                    t2 = iniside.pop(0)
                    y += 1
                    this=w
                    genquad(op, t1, t2, w)
        some=symbol()
        pinakas.append(symbol())
        table_of_expression.append(symbol())
        get_token()
        counter = counter + 1
    table_of_expression.append(symbol())
    t=0
    # if the length of table pinakas is equal to 1 then instantly get the solution
    if len(pinakas)==1:
        w=pinakas.pop(0)
        asm.write("\t li" + str(w)+ '\n')
    # if the counter is an odd number then i put the numbers in different order in the genguad than the even number checking
    if counter % 2 == 1 and len(pinakas) != 0:
        t1 = pinakas.pop(0)
        w = newtemp()
        op = pinakas.pop(0)
        t2 = pinakas.pop(0)
        genquad(op, t1, t2, w)
        if op == '+':
            asm.write("\t add" + str(t1) + ',' + (t2) + ',' + (w) + '\n')
        elif op == '-':
            asm.write("\t sub" + str(t1) + ',' + (t2) + ',' + (w) + '\n')
        elif op == '/':
            asm.write("\t div" + str(t1) + ',' + (t2) + ',' + (w) + '\n')
        elif op == '*':
            asm.write("\t mul" + str(t1) + ',' + (t2) + ',' + (w) + '\n')
        # if the counter is an even number then i put the numbers in different order in the genguad than the odd number checking
    if counter % 2 == 0 and len(pinakas) != 0:
        t1 ='T_'+str(temporary)
        w = newtemp()
        t2 = pinakas.pop(0)
        op = pinakas.pop(0)
        genquad(op, t1, t2, w)
        if op == '+':
            asm.write("\t add" + str(t1) + ',' + (t2) + ',' + (w) + '\n')
        elif op == '-':
            asm.write("\t sub" + str(t1) + ',' + (t2) + ',' + (w) + '\n')
        elif op == '/':
            asm.write("\t div" + str(t1) + ',' + (t2) + ',' + (w) + '\n')
        elif op == '*':
            asm.write("\t mul" + str(t1) + ',' + (t2) + ',' + (w) + '\n')
    # I continue to check if there is more varables in the table pinakas and do the exact same thing as above
    while len(pinakas) != 0:

        if counter % 2 == 0:
            t1 = w
            w = newtemp()
            t2 = pinakas.pop(0)
            op = pinakas.pop(0)
            genquad(op, t1, t2, w)
            if op == '+':
                asm.write("\t add" + str(t1) + ',' + (t2) + ',' + (w) + '\n')
            elif op == '-':
                asm.write("\t sub" + str(t1) + ',' + (t2) + ',' + (w) + '\n')
            elif op == '/':
                asm.write("\t div" + str(t1) + ',' + (t2) + ',' + (w) + '\n')
            elif op == '*':
                asm.write("\t mul" + str(t1) + ',' + (t2) + ',' + (w) + '\n')
        if counter % 2 == 1:
            t1=w
            w=newtemp()
            op=pinakas.pop(0)
            t2=pinakas.pop(0)
            genquad(op, t1, t2, w)
            if op == '+':
                asm.write("\t add" + str(t1) + ',' + (t2) + ',' + (w) + '\n')
            elif op == '-':
                asm.write("\t sub" + str(t1) + ',' + (t2) + ',' + (w) + '\n')
            elif op == '/':
                asm.write("\t div" + str(t1) + ',' + (t2) + ',' + (w) + '\n')
            elif op == '*':
                asm.write("\t mul" + str(t1) + ',' + (t2) + ',' + (w) + '\n')

    genquad(':=', w, '_', name_of_assi) # here i put the final conclusion to be equal to the orginal left sided name

# The for case method of cimple
def forcaseStat():
    global table_of_contisions

    if symbol()=='forcase':
        get_token()
        while symbol()=='case':
            get_token()
            if symbol() =='(':
                asm.write("L"+count()+":\n")
                get_token()

                condition()
                c.write("for ("+convert(table_of_contisions)+"){\n")
                if symbol() !=')':
                    print("Line:", lines(), "Symbol:", symbol())
                    return exit("Error  ')' was expected")
                get_token()
                statements()
                t=makelist(nextquad())
                genquad('jumb','_','_','_')
                asm.write("L" + count() + ":\n")
                n=nextquad()
                backpatch(t,n)
                asm.write("\t j "+str(n)+"\n")

            else:
                print("Line:", lines(), "Symbol:", symbol())
                return exit("Error  '(' was expected")

        if symbol() == 'default':
            get_token()
            statements()
            n=nextquad()
            backpatch(t,nextquad())
            asm.write("\t j " + str(n) + "\n")
            c.write("}\n")
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error  wrong layout of the forcase case")

def formalparlist():
    formalparitem()
    while symbol()==',':
        get_token()
        formalparitem()

# i check for the subprograms if there are IDs where put right if not error
def formalparitem():
    global formalist,names_var
    y=Entity()
    y.type='par'
    if symbol()=='in':

        get_token()
        names_var += symbol()
        names_var += " "
        y.FormalParameter.mode='cv'
        y.FormalParameter.offset=offset()
        formalist.append(symbol())
        genquad('par',symbol(),'cv','_')
        if family()=='ID':
            get_token()
            formalist.append(symbol())
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error  ID was expected")
    elif symbol()=='inout':
        y.type='ref'
        formalist.append(symbol())
        get_token()
        names_var += symbol()
        names_var += " "
        y.FormalParameter.mode = 'REF'
        y.FormalParameter.offset = offset()
        formalist.append(symbol())
        genquad('par', symbol(), 'REF', '_')
        if family()=='ID':
            get_token()
            formalist.append(symbol())
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error  ID was expected")
    else:
        print("Line:", lines(), "Symbol:", symbol())
        return exit("Error  ID was expected or an extra , was found")
    newEntity(y)

# the incase method of cimple
def incaseStat():
    global counting

    if symbol()=='incase':
        get_token()
        while symbol()=='case':
            get_token()
            if symbol()=='(':
                get_token()
                asm.write('L:' + count() + '\n')
                condition()
                if symbol()!=')':
                    print("Line:", lines(), "Symbol:", symbol())
                    return exit("Error  ) was expected")
                get_token()
                statements()
                t=makelist(nextquad())
                genquad('jumb','_','_','_')
                n=nextquad()
                backpatch(mergel(t,n),nextquad())
                asm.write('L:' + count() + '\n')
                asm.write("\t j "+str(n)+"\n")
            else:
                print("Line:", lines(), "Symbol:", symbol())
                return exit("Error  ( was expected")

# i check if the input its correctly put without errors
def inputStat():
    global counting
    if symbol()=='input':
        get_token()
        if symbol()=='(':
            get_token()
            genquad('in',symbol(),'_','_') # if there is a input command i put 'in' in the genquad table
            asm.write('L:'+count() + '\n') # puts a new label for input
            asm.write('\t li $a7,5 \n') # This is the standarize commant for input in assembly the number of the input it will be saved in the a7
            storevr('$a7',sreg())
            asm.write('\t ecall \n')  # ends the label
            if family() =='ID':
                c.write('\t scanf("%d",&' + symbol() + ');\n') # to convert the right input to a C file
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

# the fuctions print check of cimple
def printStat():
    global counting,reg,some,table_of_expression
    if symbol()=='print':
        get_token()
        if symbol()=='(':

            get_token()


            expression()
            table_of_expression.pop(0)

            c.write("\t printf("+convert(table_of_expression)+'\n')
            table_of_expression.clear()
            genquad('out', '_', '_', '_')  # if there is a print i put it inside the genquad
            asm.write("L" + count() + ":\n") # writes the label number thats gonna print
            asm.write("\t li $a0 , 1 \n") # writes the right command for print in the assembly
            loadvr(some,'$a0')
            asm.write("\t ecall \n")#end of the print label

            if symbol()!=';':
                print("Line:", lines(), "Symbol:", symbol())
                return exit("Error  ; was expected")
            get_token()
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error  ( was expected")

# the fuctions return check of cimple
def returnStat():
    global check_fun,counting,some,table_of_expression

    if symbol()=='return':
        get_token()
        check_fun=True
        if symbol()=='(':
            get_token()
            genquad('retv',symbol(),'_','_') # puts the return statment in the genquad table

            expression()
            table_of_expression.pop(0)
            c.write("\t return ("+convert(table_of_expression)+';\n')# writes it for the C file
            table_of_expression.clear()
            asm.write("L" + count() + ": \n") # label of input in assembly
            loadvr(some,tregisters())
            asm.write("\t lw $ra,-0($sp)\n")
            asm.write("\t jr $ra \n")

            if symbol()!=';':
                print("Line:", lines(), "Symbol:", symbol())
                return exit("Error  ; was expected")
            get_token()
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error  ( was expected")

def blockstatements():

    if family()=='Keyword' or family()=='ID':
        statements()
        while symbol()!='}'and (family()=='Keyword' or family()=='ID'):
            statements()

# checks if the right group symbols and delimeters was in there place and calls the rest of the statements
def statements():

    if symbol()=='{':
        get_token()
        statement()
        while symbol()!='}'and( family()=='Keyword' or family()=='ID'):
            if symbol() == 'function' or symbol() == 'procudure':
                subprograms()
            statement()

        if symbol() !='}':
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error a } was expected")

    if family()=='ID' or family()=='Keyword':

        statement()

# am checking what kind of subprogram i have and if its correctly put
def subprogram():
    global check_fun, meh, i,scopes,formalist
    y=Entity()
    scopes.Level=scopes.Level+1
    scopes.listlevel=scopes.listlevel.append(scopes.Level)
    if symbol() == 'function':
        get_token()
        if family() == 'ID':

            y.function.name=symbol()
            meh.append(symbol()) # table of the names of each fuction or prosedure
            genquad('begin_block', meh[i], '_', '_')
            asm.write('L'+count()+':\n')
            asm.write('\t sw $ra,-0($sp)\n')
            i = i + 1
            get_token()
            if symbol() == '(':
                get_token()

                formalparlist()

                c.write("\tint " +  "( "+convert(formalist)+";\n")
                if symbol() == ')':
                    get_token()
                    framelength()

                    block()

                genquad('halt', '_', '_', '_')
                i = i - 1
                genquad('end_block', meh[i], '_', '_')
                asm.write('L' + count() + ':\n')
                asm.write('\t lw $ra,-0($sp)\n')
                asm.write('\t jr $ra\n')
                scopes.Level=scopes.Level-1
                newEntity(y)
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
        y = Entity()
        scopes.Level = scopes.Level + 1
        scopes.listlevel = scopes.listlevel.append(scopes.Level)
        get_token()
        if family() == 'ID':
            y.function.name = symbol()
            meh.append(symbol())

            genquad('begin_block', meh[i], '_', '_')
            asm.write('L' + count() + ':\n')
            asm.write('\t sw $ra,-0($sp)\n')
            i = i + 1

            get_token()
            if symbol() == '(':
                get_token()
                formalparlist()
                c.write("int " + str(symbol()) + "(" + str(formalist) + "){\n")
                if symbol() == ')':
                    get_token()
                    framelength()
                    block()
                genquad('halt', '_', '_', '_')
                i = i - 1
                genquad('end_block', meh[i], '_', '_')
                asm.write('L' + count() + ':\n')
                asm.write('\t lw $ra,-0($sp)\n')
                asm.write('\t jr $ra\n')
                scopes.Level = scopes.Level - 1
                newEntity(y)
                if check_fun == False:
                    print("Line:", lines(), "Symbol:", symbol())
                    return exit("Error you need a return statement in the procedure")
            else:
                print("Line:", lines(), "Symbol:", symbol())
                return exit("Error ) group symbol was expected")
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error the group symbol ( was expected")

# a while so i can get all the fuctutions and procecuders
def subprograms():
    while symbol()=='function' or symbol()=='procedure':
        subprogram()

# a switch case of the cimple language
def switchcaseStat():
    global counting,table_of_contisions,table_of_expression
    if symbol()=='switchcase':
        c.write("switch{\n")
        get_token()
        while symbol()=='case':
            c.write("\t case")
            get_token()
            if symbol() =='(':
                get_token()
                condition() # every condition after it finishes it has getotken to get the next one
                c.write(str(table_of_contisions))
                table_of_contisions.clear()
                asm.write("L"+count()+":\n")
                if symbol() !=')':
                    print("Line:", lines(), "Symbol:", symbol())
                    return exit("Error  ) was expected")
                get_token()
                statements()
                n=makelist(nextquad())
                genquad('jumb','_','_','_')
                asm.write("L" + count() + ":\n")
                n2=nextquad()
                x=mergel(makelist(nextquad()),e)
                asm.write("\t j"+str(n2)+"\n")
                c.write("\t break;")
            else:
                print("Line:", lines(), "Symbol:", symbol())
                return exit("Error  ( was expected")
        if symbol() == 'default':
            get_token()
            statements()
            t=nextquad()
            t2=nextquad()
            backpatch(x,t)
            backpatch(n,t2)
            asm.write("L" + count() + ":\n")
            asm.write("\t j" +str(t2)+ "\n")
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error case wrong look again the layout of the switch case")

def chec():
    global checking_contion,table_of_contisions

    table_of_contisions.clear()
    checking_contion=True

# a while of the cimple language
def whileStat():
    global counting,checking_contion,table_of_contisions
    if symbol()=='while':

        get_token()
        if symbol() =='(':
            j.append(nextquad())
            asm.write("L" + count() + ":\n")
            get_token()
            c.write("While (")
            condition()
            c.write(str(table_of_contisions)+'){\n')
            if symbol()==')':
                get_token()
                statements()
                n = j.pop()
                while checking_contion==False:
                    genquad('jumb','_','_',n)
                    asm.write("L" + count() + ":\n")
                    asm.write("\t j"+str(n)+"\n")
                    chec() # i will change the checking_contision to fit if the contions are true after a while so i can exit

                c.write("}")

            else:
                print("Line:", lines(), "Symbol:", symbol())
                return exit("Error ) was expected")
        else:
            print("Line:", lines(), "Symbol:", symbol())
            return exit("Error a  ( was expected")

def nextquad(): # gives the number of the current label number
    global num,numbering,next_num

    numbering.append(num)
    next_num=next_num +1

    return num

def genquad(op, x, y, z): # a fuction that allows as to put the commands in the right order
    global num,inside,newtups
    newtups.append(list([num,op,x,y,z]))
    inside.append(tuple((num,op,x,y,z)))
    num=num+1

    return inside

def newtemp(): # i create the next new temporary vareble
    global temporary
    T='T_'+str(temporary)
    temporary = temporary + 1

    # THIS DOESNT WORK
    # I use this to start the symbol table but there is a problem with the offset fuction


    y=Entity()
    y.type='temp'
    y.FormalParameter.offset=offset()
    y.name=T
    newEntity(y)

    return T

def emptylist(): # use it to create an empty list
    global empty_List
    empty_List=list()
    return empty_List

def makelist(x): # i get a varble and put it inside the list_label list
    global label_list
    label_list=list()
    label_list.append(x)

    return label_list

def mergel(list1, list2): #I merge 2 lists together
    list1=list1+list2
    return list1

def backpatch(lists,z): # I check if the last element of the list of tuples is equal to '_'
                        # i change it to the right label to jumb in to or wait until the end of a command of the cimple program to put the right numbered lable

    global inside,e,a,nums,newtups,jumblist

    nums=0
    t=0
    for i in range(len(newtups)-1):
        nums=nums + 1
        y=0
        for j in range(len(lists)-1):
            if newtups[nums][0]==lists[y] and newtups[nums][1]!='jumb' and newtups[nums][4]=='_':
                newtups[nums][4]=z
                t=1
            if newtups[nums][1]=='jumb' and newtups[nums][4]=='_' and ifch==True:
                newtups[nums][4]=z

            y=y+1

    return newtups



if __name__ == '__main__':

    tokens=matrix()
    syntax_analyzer()
    newtups.pop(0)
    f = open("test.int", "w")
    for i in range(len(newtups)):
        f.write(str(newtups[i][0])+': ')
        f.write(str(newtups[i][1])+', ')
        f.write(str(newtups[i][2]) + ', ')
        f.write(str(newtups[i][3]) + ', ')
        f.write(str(newtups[i][4]) + '\n')
    f.close()
    k=[]
    t=''
    f = open("test.symb","w")
    for j in names_var:
        t+=j
        if j==' ':
            k.append(t)
            t=''
    for i in range(len(k)):
        t=scopes.enList[i]

        f.write('Scope:' + str(k[i]) + '\t' + 'Level Of Nesting:' + str(scopes.Level) + '\n')
        f.write('Entity:'+str(t) +'\t')
        f.write('Offset:'+ str(off[i])+'\n')
        f.write('\n')
    f.close()
    c.close()
    asm.close()





