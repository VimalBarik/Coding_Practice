#include <stdio.h>

int main(void)
{
    float S, n;
    char operator;
    printf("Enter the accumulator: ");
    scanf("%f", &S);

    printf("= %f\n", S);

    scanf("%f  %c", &n, &operator);

    if (operator== '+')
        printf("%f\n", S + n);

    else if (operator== '-')
        printf("%f\n", S - n);

    else if (n == 0 && operator== '/')
        printf("Division by Zero\n");

    else if (operator== '/')
        printf("%f\n", S / n);

    else if (operator== '*')
        printf("%f\n", S * n);

    else if (operator== 'E')
        printf("End of Calculations\n");

    else
        printf("Invalid output");
}