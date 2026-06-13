#include <stdio.h>

int main(void)
{
    int n = 0, number, triangularNumber, counter = 1;

    while (counter <= 5)
    {

        printf("What triangular number do you want?");
        scanf("%i", &number);

        triangularNumber = 0;
        n = 0;

        while (n <= number)
        {
            triangularNumber += n;
            n++;
        }

        printf("Triangular number %i is %i\n\n", number, triangularNumber);

        counter++;
    }
    return 0;
}