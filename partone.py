#Panagiotis Mouzouris 4561 cs04561
#Serafim Themistokleous 4555 cs04555

import string
import sys

global indexer, tokens

tokens = []

indexer = []


def split_to_char(word):
    return [char for char in word]

def matrix(count):
    comment = 0
    f = open("Ate.txt", "r")

    # ALL LINES IN ONE STRING
    allLinesInOne = f.read()

    #print(allLinesInOne)

    # ALL LINES SEPARATED IN LIST
    lines_list = allLinesInOne.split("\n")

    #print(linies_list)


    keywords_list = {'program':'Keyword', 'declare':'Keyword', 'if':'Keyword', 'else':'Keyword', 'while':'Keyword', 'switchcase':'Keyword', 'forcase':'Keyword', 'incase':'Keyword', 'case':'Keyword', 'default':'Keyword', 'not':'Keyword', 'and':'Keyword','or':'Keyword', 'function':'Keyword', 'procedure':'Keyword', 'call':'Keyword', 'return':'Keyword', 'in':'Keyword', 'inout':'Keyword', 'input':'Keyword', 'print':'Keyword'}
    symbols_list = {'(':'Symbol', ')':'Symbol','{':'Symbol', '}':'Symbol','[':'Symbol', ']':'Symbol'}
    numbers_list={'1':'Number','2':'Number','3':'Number','4':'Number','5':'Number','6':'Number','7':'Number','8':'Number','9':'Number','0':'Number'}
    operators_list={'+':'addOp','-':'addOp','*':'mulOp','/':'mulOp','==':'relOp','>=':'relOp','<':'relOp','>':'relOp','<>':'relOp','<=':'relOp'}
    assign_list = {':=': 'Assignment'}
    delimiter_list = {',': 'Delimiter', '.': 'Delimiter', ';': 'Delimiter'}
    alphabet_list = {'a':'ID','b':'ID','c':'ID','d':'ID','e':'ID','f':'ID','g':'ID','h':'ID','i':'ID','j':'ID','k':'ID','l':'ID','m':'ID','n':'ID','o':'ID','p':'ID','q':'ID','r':'ID','s':'ID','t':'ID','u':'ID','v':'ID','w':'ID','x':'ID','y':'ID','z':'ID','A':'ID','B':'ID','C':'ID','D':'ID','E':'ID','F':'ID','G':'ID','H':'ID','I':'ID','J':'ID','K':'ID','L':'ID','M':'ID','N':'ID','O':'ID','P':'ID','Q':'ID','R':'ID','S':'ID','T':'ID','U':'ID','V':'ID','W':'ID','X':'ID','Y':'ID','Z':'ID'}  # The alphabet combine in a list

    keywords = keywords_list.keys()
    symbols = symbols_list.keys()
    numbers = numbers_list.keys()
    operators = operators_list.keys()
    assignment = assign_list.keys()
    delimiters = delimiter_list.keys()
    alphabet = alphabet_list.keys()

    for i in range(len(lines_list)):
        j = 0
        count += 1 #count lines
        splt = lines_list[i]
        temporary = ""

        characters = split_to_char(splt)
        print(characters)

        #for j in range(0,len(characters)):
        while j < (len(characters)):
            if characters[j] == "#":
                comment = comment + 1
            else:
                if (comment % 2) == 0 :
                    temporary = temporary + characters[j]
                    temporary = "".join(temporary)

                    if characters[j].isspace():
                        j = j + 1

                    if characters[j] not in keywords and characters[j] not in symbols and characters[j] not in numbers and characters[j] not in operators and characters[j] not in assignment and characters[j] not in delimiters and characters[j] not in alphabet and characters[j] != "\n" and characters[j].isspace()==False and characters[j] != "." and characters[j] != "#" and characters[j] != "\t" and characters[j]!=":":
                        print("Line:", count, "Symbol:", characters[j])  # first i check in the token its in range of the liegal tokens in the cimple program
                        return exit("Error Symbol Was Not recognized")

                    if characters[j] == ".":  # this marks the end of the program
                        tokens.append([".", count, "EOF"])

                    if characters[j] in symbols:  # here i save with a counter for each group symbol if the counter is even then there is no errors
                        if characters[j] == "}" and characters[j + 1] != ".":
                            print("Line:", count, "Symbol:", characters[j])
                            return exit("Error Symbol has to end with a . delimeter")
                        elif characters[j] == "{":
                            # sympol += 1
                            print("'" + temporary + "'" + " IS SYMBOL")
                            temporary = ""
                            tokens.append([characters[j], count, "Symbol"])
                            break
                        elif characters[j] == "(" or characters[j] == ")":
                            #sympol += 1
                            print("'" + temporary + "'" + " IS SYMBOL")
                            temporary = ""
                            tokens.append([characters[j], count, "Symbol"])
                            j = j + 1

                    if characters[j] == ":":
                        if characters[j+1] == "=":
                            print("':=' IS ASSIGNMENT")
                            temporary=""
                            tokens.append([":=",count,"Assignment"])
                            j = j + 1
                        else:
                            print("ERROR")
                            return exit(0)
                        j = j + 1

                    if characters[j] in numbers:
                        if characters[j+1] not in numbers:
                            print("'" + characters[j] + "'" + " IS NUMBER")
                            tokens.append([temporary, count, "Number"])
                            temporary = ""
                            j = j + 1
                        else:
                            j = j + 1

                    if characters[j] in delimiters:  # if there is a delimiter to make it token and check for errors
                        if characters[j] == ";": #and characters[j + 1] != "@":
                            print("'" + ";" + "'" + " IS DELIMITER")
                            temporary = ""
                            tokens.append([characters[j], count, "Delimiter"])
                            break
                            #print("Line:", count, "Symbol:", characters[j])
                            #return exit("Error every line has to end with ;")
                        elif characters[j] == ",":
                            print("'" + temporary + "'" + " IS DELIMITER")
                            temporary = ""
                            tokens.append([characters[j], count, "Delimiter"])
                            j = j + 1

                    if characters[j] in alphabet:
                        temporary = ""
                        loop = True

                        while loop:
                            temporary = temporary + characters[j]
                            temporary = "".join(temporary)

                            #if characters[j+1] not in alphabet and characters[j+1] not in numbers:
                              #  loop = False

                            if temporary in keywords:

                                if temporary == "in" and characters[j+1] == "p":
                                    temporary = "input"

                                    print("'" + temporary + "'" + " IS KEYWORD")
                                    tokens.append([temporary, count, "Keyword"])
                                    print("en dame")
                                    length = split_to_char(temporary)
                                    j = len(length) - 1
                                    temporary = ""
                                    loop = False
                                else:
                                    print("'" + temporary + "'" + " IS KEYWORD")
                                    tokens.append([temporary,count,"Keyword"])
                                    length = split_to_char(temporary)
                                    j = len(length)-1
                                    temporary = ""
                                    loop = False
                            elif (characters[j] in alphabet or characters[j] in numbers) and (characters[j+1] in delimiters or characters[j+1] in symbols or characters[j+1] == ":"):
                                if len(split_to_char(temporary)) < 31:
                                    print("'" + temporary + "'" + " IS ID")
                                    tokens.append([temporary,count,"ID"])
                                    temporary = ""
                                    loop = False
                                else:
                                    print("Line:", count, "Idendifier:", temporary)
                                    return exit("Error Idendifier very long")

                            j = j + 1

def main():
    matrix(0)

main()