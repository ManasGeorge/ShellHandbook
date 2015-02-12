#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>

int main(int argc, char* argv[])
{
    int i;
    if(argc < 2){
        exit(0);
    }

    char buffer[1024], shellcode[512];
    buffer[1023] = 0;
    strncpy(buffer,argv[1],1023);

    for(i = 0; i < 1023; i+=2){
        char digit[3] = {buffer[i], buffer[i+1], 0};
        shellcode[i/2] = (char)strtol(digit, NULL, 16);
    }

    void (*ret)(void);
    ret = (void (*)(void))shellcode;
    ret();
}
