#include <stdio.h>

int main()
{
    int n;
    printf("Enter Number: \n");
    scanf("%d", &n);

    int fact = 1;
    for (int i = 1; i <= n; i++)
    {
        fact = fact * i;
    }
    printf("%d\n", fact);
}