#!/bin/python2
import sys
from subprocess import call, check_output
from os import remove

def main():
    if len(sys.argv) != 2:
        print "Outputs the shellcode for a given asm file"
        print "Usage: ./opcodes.py <file>"
        print "The filename supplied must be without the .asm extension"
        exit(1)

    f = sys.argv[1]
    if call("nasm -f elf64 " + f + ".asm", shell=True):
        print "Assembler error"
        sys.exit(1)
    remove(f)

    if call("ld -o" + f + " " + f + ".o", shell=True):
        print "Linker error"
        sys.exit(1)

    disas = check_output("objdump -d " + f + ".o", shell=True)
    # Trim the top and last line
    disas = "\n".join(disas.split("\n")[7:-1])
    opcodes = ""
    shellcode = ""
    for line in disas.split("\n"):
        opline = line[6:20]
        opcodes += "".join(opline.split())
        opline = "".join(map((lambda x: "\\x"+x),opline.split()))
        shellcode += '"' + opline + '"' + "\n" 
    print opcodes
    print shellcode
    remove(f + ".o")

if __name__ == "__main__":
    main()
