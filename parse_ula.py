from __future__ import print_function
from ply import yacc
from lex_ula import tokens
#Adapted by Alan Berman
import os
import sys


start = "Start"
#list of variables
ids=[]
#list of variable values
vals=[]
def p_start(p):
    """Start : Program"""
    #p[0] = ["Start", [p[1]]]
    p[0] = p[1]


def p_program_statements(p):
    """Program : Statements"""
    #["Program", p[1]]
    p[0] = p[1]


def p_statements(p):
    """Statements : Statements Statement
                    | Statement"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_statement(p):
    """Statement : ID '=' expression"""
    p[0] = ["=", [p[1]], p[3]]
    #if the variable has already been created
    if p[1] in ids:
         print( "semantic error on line"+" "+str(p.lineno(1)-2))
         filename=sys.argv[1][:-3]
         filename+="err"
         output = open(filename,'w')
         output.write( "semantic error on line"+" "+str(p.lineno(1)-2))
         output.close()
         sys.exit()
    #if a value exists but its variable doesn't
    elif p[3] in vals and p[1] not in vals:
        print( "semantic error on line"+" "+str(p.lineno(1)-2))
        filename=sys.argv[1][:-3]
        filename+="err"
        output = open(filename,'w')
        output.write( "semantic error on line"+" "+str(p.lineno(1)-2))
        output.close()
        sys.exit()
    #add the variable and its value to the lists
    else:
        ids.append(p[1])
        vals.append(p[3])





def p_expression_plus(p):
    """expression : expression '@' term"""
    p[0] = ["@", p[1], p[3]]


def p_expression_minus(p):
    """expression : expression '$' term"""
    p[0] = ["$", p[1], p[3]]


def p_expression_term(p):
    """expression : term"""
    p[0] = p[1]


def p_term_multiply(p):
    """term : term '#' factor"""
    p[0] = ["#", p[1], p[3]]


def p_term_divide(p):
    """term : term '&' factor"""
    p[0] = ["&", p[1], p[3]]


def p_term_factor(p):
    """term : factor"""
    p[0] = p[1]


def p_factor_expression(p):
    """factor : '(' expression ')'"""
    p[0] = p[2]


def p_factor_float(p):
    """factor : FLOAT_LITERAL"""
    p[0] = [p[1]]


def p_factor_id(p):
    """factor : ID"""
    p[0] = [p[1]]
    #if a variable has not been assigned a value
    if p[1] not in ids:
        print( "semantic error on line"+" "+str(p.lexer.lineno-1))
        filename=sys.argv[1][:-3]
        filename+="err"
        output = open(filename,'w')
        output.write( "semantic error on line"+" "+str(p.lexer.lineno-1))
        output.close()
        sys.exit()



def p_error(p):
    print( "parse error on line"+" "+str(p.lexer.lineno))
    filename=sys.argv[1][:-3]
    filename+="err"
    output = open(filename,'w')
    output.write( "parse error on line"+" "+str(p.lexer.lineno))
    output.close()
    sys.exit()


def print_tree(outfile, tupletree, depth=0):
    #print("\t"*depth, tupletree[0], sep="", file=outfile)
    #print("\t"*depth, tupletree[0])
    for item in tupletree[1]:
        if isinstance(item, tuple):
            print_tree(outfile, item, depth + 1)
       # else:
        #    print("\t"*(depth+1), item, sep="", file=outfile)
         #   print("\t"*(depth+1), item)


parser = yacc.yacc()


def main():
    if len(sys.argv) == 2:
        infilename = sys.argv[1]
        if os.path.isfile(infilename):
            infile = open(infilename, "r")
            syntree = parser.parse(infile.read())

            #print(syntree)
           # outfilename = os.path.splitext(infilename)[0]+".ast"
            #with open(outfilename, "w") as outfile:
            #    print_tree(outfile, syntree)

      #  else:
    #        print("Not a valid file")
    #else:
       # print("Specify filename, e.g. parse_ula.ply my_program.ula")
#

#if __name__ == "__main__":
 #   main()
