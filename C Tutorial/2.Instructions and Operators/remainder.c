#include<stdio.h>

int main(){
    int number;
    printf("Enter the number: \n");
    scanf("%i", &number);

    int remainder = number%2;
    printf("%i\n", remainder==0);
}