// Program to generate and display a table of n and n²
#include <stdio.h>

int main()
{
    int n;

    printf("Enter the value of n:    ");
    scanf("%d", &n);

    printf(" n        n²\n");

    for (int i = 1; i <= n; i++)
    {
        if (n <= 10 && n >= 1)
        {
            printf("%2i        %i\n", i, i * i);
        }
        else
        {
            printf("Invalid Value\n");
        }
    }
}