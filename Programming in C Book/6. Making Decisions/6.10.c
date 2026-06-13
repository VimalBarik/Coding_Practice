// Program to generate a table of prime numbers

#include <stdio.h>

int main(void)
{
    int p, d;
    _Bool isprime;

    for (p = 2; p <= 50; ++p)
    {
        isprime = 1;

        for (d = 2; d < p; ++d)
            if (p % d == 0)
                isprime = 0;

        if (isprime != 0)
            printf("%i ", p);
    }
    printf("\n");
    return 0;
}