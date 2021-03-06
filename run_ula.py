from __future__ import print_function

#Adapted from http://llvmlite.pydata.org/en/latest/binding/examples.html#compiling-a-trivial-function
#Author: Alan Berman
#24/9/15
import ir_ula
import parse_ula
import sys
from ctypes import CFUNCTYPE, c_double, c_float

import llvmlite.binding as llvm
import sys
#import parse_ula
from ir_ula import module
# All these initializations are required for code generation!
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()  # yes, even this one



def create_execution_engine():
    """
    Create an ExecutionEngine suitable for JIT code generation on
    the host CPU.  The engine is reusable for an arbitrary number of
    modules.
    """
    # Create a target machine representing the host
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    # And an execution engine with an empty backing module
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
    return engine


def compile_ir(engine, llvm_ir):
    """
    Compile the LLVM IR string with the given engine.
    The compiled module object is returned.
    """
    # Create a LLVM module object from the IR
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()
    # Now add the module and make sure it is ready for execution
    engine.add_module(mod)
    engine.finalize_object()
    return mod

llvm_ir = str(module)
engine = create_execution_engine()
mod = compile_ir(engine, llvm_ir)

    # Look up the function pointer (a Python int)
func_ptr = engine.get_function_address("main")

    # Run the function via ctypes
cfunc = CFUNCTYPE(c_float)(func_ptr)
res = cfunc()
print(res)
filename=sys.argv[1][:-3]

filename+="run"
output = open(filename,'w')
output.write(str(res))
#if __name__ == "__main__":
    #main(sys.argv[1])