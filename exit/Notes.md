Wrote shellcode in asm, compiled and checked to see if it worked (strace)
Extracted opcodes, packaged into shellcode, put in C-file
Compiled C file without stack protection and with an executable stack
Seems to work (exits normally in gdb, but strace doesn't show anything)
