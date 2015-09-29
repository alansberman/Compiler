from __future__ import print_function
from ply import lex
import os
import sys
#Adapted by Alan Berman
tokens = ["ID", "FLOAT_LITERAL", "WHITESPACE", "COMMENT"]

literals = ["@", "$", "#", "&", "=", "(", ")"]

t_FLOAT_LITERAL = r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'

def t_WHITESPACE(t):
    r'\s*(\p{P})?\s'
    t.lexer.lineno += t.value.count("\n") # line number tracking for exception handling
    if __name__ == "__main__":
        return t

def t_COMMENT(t):
    r'/\*(.|[\r\n])*?\*/|(//.*)'
    # regex allows for /* */ and // comments but also allows extra *s in a multiline /* */ comment
    t.lexer.lineno += t.value.count("\n") # implement line number tracking
    if __name__ == "__main__":
        return t

def t_ID(t):
    r'[_a-zA-Z][_a-zA-Z0-9]*'
    return t

def t_error(t):
    t.lexer.skip(1)
    return "lexical error on line"+" "+str(t.lexer.lineno)
lexer = lex.lex()

def main():
    if len(sys.argv) == 2:
        infilename = sys.argv[1]
        if os.path.isfile(infilename):
            infile = open(infilename, "r")
            lexer.input(infile.read())
            outfilename = os.path.splitext(infilename)[0]+".tkn"
            outfile = open(outfilename, "w")

            for token in lexer:
                #if we've found an error
                if (type(token) is str):
                    return token

            outfile.close()
        else:
            print("Not a valid file")
    else:
        print("Specify filename, e.g. lex_ula.ply my_program.ula")

#if __name__ == "__main__":
 #   main()
