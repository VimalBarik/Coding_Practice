#include <stdio.h>

int main(void)
{
    int number, triangularNumber = 0, m, same = 0;

    printf("How many Input do you want? \n");
    scanf("%i", &m);

    for (int i = 1; i <= m; ++i)
    {

        printf("What triangular number do you want?");
        scanf("%i", &number);

        triangularNumber = 0;

        if (same != number)
        {
            for (int j = 1; j <= number; ++j)
                triangularNumber += j;

            printf("Triangular number %i is %i\n\n", number, triangularNumber);
        }

        else
        {
            printf("Number alrady used\n");
        }
        same = number;
    }
    return 0;
}