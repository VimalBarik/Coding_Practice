// Program to print a table of first 10 factorials
#include <stdio.h>

int main()
{
    int i, fact = 1;

    for (i = 1; i <= 10; i++)
    {
        fact = fact * i;
        printf("%d\n", fact);
    }
    return 0;
}