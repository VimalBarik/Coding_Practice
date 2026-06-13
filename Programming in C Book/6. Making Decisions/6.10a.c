// Program to generate a table of orime numbers.

#include <stdio.h>
#include <stdbool.h>

int main(void)
{
    int p, d;
    bool isprime;

    for (p = 2; p <= 50; ++p)
    {
        isprime = true;

        for (d = 2; d < p; ++d)
            if (p % d == 0)
                isprime = false;

        if (isprime != false)
            printf("%i   ", p);
    }
    printf("\n");
    return 0;
}