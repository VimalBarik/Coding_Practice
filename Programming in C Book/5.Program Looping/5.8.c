//Prorgam to reverse the digits of a number
#include<stdio.h>

int main(){

    long number, i, right_digit;

    printf("Enter Number: \n");
    scanf("%ld", &number);

    while (number != 0)
    {
        right_digit = number%10;
        printf("%ld", right_digit);
        number = number/10;
    }
    printf("\n");
}