#Author: Alan Berman
#24/9/15
import sys
import parse_ula
from llvmlite import ir
arg = open(sys.argv[1], "r")
parser = parse_ula.parser
parseTree = parser.parse(arg.read())
#Add "Program" to the front of the list so that code_gen runs
parseTree.insert(0,"Program")
last_var = "" # keeps track of the last var assigned
var_dict = {}  # var names associated with memory location

#Check for float literals
#if castable, is a float
def isFloat(f):
    try:
        float(f)
        return True
    except(ValueError):
        return False

# @ for addition, $ for subtraction, # for multiplication and & for division.
def code_gen(tree): # traverse tree recursively to generate code
    global last_var
    #print(tree)
    if tree[0] == "Program":
        for t in tree[1:]:
            code_gen(t)
    elif tree[0] == "=":
        last_var = tree[1][0]
        var_dict[last_var] = builder.alloca(ir.FloatType())
        builder.store(code_gen(tree[2]), var_dict[last_var])
    elif tree[0] == "@":
        return(builder.fadd(code_gen(tree[1]),code_gen(tree[2])))
    elif tree[0] == "$":
        return(builder.fsub(code_gen(tree[1]),code_gen(tree[2])))
    elif tree[0] == "#":
        return(builder.fmul(code_gen(tree[1]),code_gen(tree[2])))
    elif tree[0] == "&":
        return(builder.fdiv(code_gen(tree[1]),code_gen(tree[2])))
    elif isFloat(tree[0]):
        return(ir.Constant(ir.FloatType(), float(tree[0])))
    #if the variable already exists in the var_dict dictionary, load it instead, rather than storing
    elif var_dict.get(tree[0]) is not None:
        return (builder.load(var_dict[tree[0]]))



flttyp = ir.FloatType() # create float type
fnctyp = ir.FunctionType(flttyp, ()) # create function type to return a float
module = ir.Module(name="ula") # create module named "ula"
func = ir.Function(module, fnctyp, name="main") # create "main" function
block = func.append_basic_block(name="entry") # create block "entry" label
builder = ir.IRBuilder(block) # create irbuilder to generate code
code_gen(parseTree)
builder.ret(builder.load(var_dict[last_var])) # specify return value
print(module)
filename=sys.argv[1][:-3]
filename+="ir"
output = open(filename,'w')
output.write(str(module))
output.close()


