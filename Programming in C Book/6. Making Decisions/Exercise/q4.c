#include <stdio.h>

int main()
{

    long number, right_digit;

    printf("Enter your number.\n");
    scanf("%ld", &number);

    

    if (number < 0)
    {
        number = number * (-1);
        do
        {
            right_digit = number % 10;
            printf("%ld", right_digit);
            number = number / 10;
        } while (number != 0);
        printf("-");
    }

    else if (number > 0)
    {
        do
        {
            right_digit = number % 10;
            printf("%ld", right_digit);
            number = number / 10;
        } while (number != 0);
    }

    printf("\n");
    return 0;
}