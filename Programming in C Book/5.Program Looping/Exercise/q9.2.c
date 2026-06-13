//5.3
#include <stdio.h>

int main()
{

    int n = 0, triangularNumber;

    printf("TABLE OF TRIANGULAR NUMBERS\n\n");
    printf("n     Sum from 1 to n\n");
    printf("---   ---------------\n");

    triangularNumber = 0;

    while (n < 10)
    {
        ++n;
        triangularNumber += n;

        printf("%2i            %i\n", n, triangularNumber);
    }
    return 0;
}