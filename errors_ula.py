import sys
import os
import lex_ula
import parse_ula


def main(argv):
    source_code_file = open(argv, "r")
    ans = lex_ula.main()
    if (ans!=None):
        print(ans)
    if (ans==None):
        parse_ula.main()

    filename=argv[:-3]

    filename+="err"
    output = open(filename,'w')
    if (ans!=None):
        output.write(ans)
    output.close()
if __name__ == "__main__":
    main(sys.argv[1])