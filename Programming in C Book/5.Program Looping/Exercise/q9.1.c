//5.2
#include <stdio.h>

int main()
{

    int n, triangular_number;

    triangular_number = 0;
    n = 1;

    while (n <= 200)
    {
        triangular_number = triangular_number + n;
        n++;
    }
    printf("The 200th triangular number is %d\n", triangular_number);
}
