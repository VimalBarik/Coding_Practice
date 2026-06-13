#include <stdio.h>

int main()
{
    int a = 1;

    for (int i = 1; i <= 10; i++)
    {
        for (int j = 1; j <= i; j++)
        {
            a = a * j;
        }
        printf("%d\n", a);
        a = 1;

    }

}