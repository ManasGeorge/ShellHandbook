#!/bin/python2
import sys
import argparse
from subprocess import call, check_output
from os import remove, getcwd

def main():
    parser = argparse.ArgumentParser(description="Generates shellcode from a nasm source file in a way that makes it easy to use in other programs and in exploits. Store the nasm source file in a folder with the same name as the file.")

    parser.add_argument("filename", help="The name of the file in which the shellcode resides, without the .asm extension.", type=str)

    parser.add_argument("-n", "--no-clean", help="Keeps the compiled files from the shellcode generation process. Useful for debugging.", action="store_true")

    parser.add_argument("-t", "--test", help="Tests the shellcode in a barebones C program", action="store_true")

    parser.add_argument("-s", "--strace-test", help="Tests the shellcode in a barebones C program, using strace to monitor system calls.", action="store_true")

    parser.add_argument("-d", "--disassemble", help="Shows the output of objdump -d on the generated shellcode.", action="store_true")

    parser.add_argument("-b", "--buffer-size", help="The length of the buffer in bytes. The distance between the start of the buffer and the start of the stored instruction pointer", type=int, default=0)

    parser.add_argument("-a", "--shellcode-array", help="Displays the shellcode as an array of integers, can be easily assigned to a character array (in gdb, for example).", action="store_true")

    parser.add_argument("-p", "--show-python", help="Forms a python command that generates the shellcode, can be copied and used as a command line argument to a program", action="store_true")

    parser.add_argument("-a", "--return-address", help="The new return address with which to overwrite the stored instruction pointer. Enter the address in hex as it is, but do not include the prefix 0x and do not convert to little endian form.", type=str, default="")

    args = parser.parse_args()

    f = args.filename
    f = sys.argv[1]
    f = f + '/' + f

    if call("nasm -f elf64 " + f + ".asm", shell=True):
        print "Assembler error"
        sys.exit(1)

    if call("ld -o" + f + " " + f + ".o", shell=True):
        print "Linker error"
        sys.exit(1)

    disas = check_output("objdump -d " + f + ".o", shell=True)
    # Trim the top and last line
    opcodes = ""
    shellcode = ""
    for line in disas.split("\n"):
        if(line and line[0] == " "):
            opline = line[6:20]
            opcodes += "".join(opline.split())
            opline = "".join(map((lambda x: "\\x"+x),opline.split()))
            shellcode += '"' + opline + '"' + "\n" 

    if args.disassemble :
        print disas

    if args.strace_test :
        call("strace " + getcwd() + "/shellcage/shellcage " + opcodes, shell=True)
    if args.test :
        call(getcwd() + "/shellcage/shellcage " + opcodes, shell=True)

    if args.show_python or args.shellcode_array:
        if args.buffer_size == 0:
            print sys.argv[0] + ': error: Must include --buffer-size with --show-python or --shellcode-array'
            sys.exit(1)
        else:
            a = args.buffer_size

        if args.return_address == "":
            print sys.argv[0] + ': error: Must include --return-address with --show-python or --shellcode-array'
            sys.exit(1)
        else:
            addr = args.return_address
            addr = [addr[x:x+2] for x in range(0,len(addr),2)]
            addr.reverse()
            addr = "".join(addr)

        if(args.show_python):
            print """$(python -c 'print ("{0}" + "90"*{1} + "{2}").decode("hex"))'""".format(opcodes,str(a),addr)

        if(args.shellcode_array):
            array = map(ord,(opcodes + "90"*a + addr).decode("hex"))
            print array

    if not args.no_clean :
        remove(f + ".o")
        remove(getcwd() + '/' + f)

    sys.exit(1)

if __name__ == "__main__":
    main()
