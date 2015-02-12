SECTION .text
    global _start

_start:
    jmp MESSAGE

PRINT:
    xor rax,rax
    mov al,1
    xor rdi,rdi
    mov dil,1
    pop rcx
    mov rsi,rcx
    xor rdx,rdx
    mov dl,6
    syscall

    xor rdi,rdi
    mov dil,0
    xor rax,rax
    mov al,60
    syscall

MESSAGE:
    call PRINT
    db "Hello"
