#include <stdio.h>

int power(int x, int y);

int main()
{
    int number, number_, digit, digit_count;

    printf("Enter number: ");
    scanf("%i", &number);

    digit_count = 0;
   number_ = number;

    do
    {
        digit = number_ % 10;
        printf("%i", digit);
        number = number_ / 10;
        digit_count++;
    } while (number_ != 0);

    printf("\n");

    printf("%i\n", digit_count);

    int y = digit_count - 1;
    int x = 10;

    printf("%i\n", power(x, y));

    float digit1;

    digit1 = number % x;
    printf("%f\n", digit1);
}

int power(int x, int y)
{

    int t = x;

    for (int i = 1; i < y; i++)
    {
        x = x * t;
    }
    return x;
}
