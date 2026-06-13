#include <stdio.h>

int main()
{
    int n;
    printf("Enter Number: \n");
    scanf("%i", &n);

    if (n % 2 == 0 || n % 3 == 0 || n % 5 == 0)
    {
        if (n != 2 && n != 3 && n != 5)
        {
            printf("Its not a Prime Number\n");
        }
        else if (n==2 || n==3 || n==5)
        {
            printf("Its a prime no.\n");
        }
    }
    else
    {
        printf("Its a prime Number\n");
    }
    return 0;
}