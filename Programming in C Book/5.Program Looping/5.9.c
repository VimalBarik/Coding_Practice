// Program to reverse the digits of a number using do while loop
#include <stdio.h>

int main()
{

    long number, right_digit;

    printf("Enter your number.\n");
    scanf("%ld", &number);

    do
    {
        right_digit = number % 10;
        printf("%ld", right_digit);
        number = number / 10;
    } while (number != 0);

    printf("\n");
    return 0;
}