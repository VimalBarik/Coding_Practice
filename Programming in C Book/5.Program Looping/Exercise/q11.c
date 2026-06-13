#include<stdio.h>

int main(){

    long number, i, right_digit;

    printf("Enter Number: \n");
    scanf("%ld", &number);

    int sum = 0;

    while (number != 0)
    {
        right_digit = number%10;
        sum = sum + right_digit;
        number = number/10;
    }
    printf("%d\n", sum);
}