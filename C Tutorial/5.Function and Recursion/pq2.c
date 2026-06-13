#include<stdio.h>

void printhello();
void printgoodbye();

int main(){

    printhello();
    printgoodbye();
    printhello();
    return 0;
}

void printhello(){
    printf("Hello world\n");
}
void printgoodbye(){
    printf("Good bye\n");
}