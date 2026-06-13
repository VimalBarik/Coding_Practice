// Program to generate triangular number using formula
#include <stdio.h>

int main()
{
    int n, triangular_number;

    for (n = 5; n <= 50; n++)
    {
        if (n % 5 != 0)
        {
            continue;
        }
        triangular_number = (n * n + n) / 2;
        printf("%d\n", triangular_number);
    }
    return 0;
}