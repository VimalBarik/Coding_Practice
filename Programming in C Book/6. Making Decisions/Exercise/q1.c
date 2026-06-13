#include <stdio.h>

int main(void)
{
    int a, b;

    printf("Enter two numbers:  \n");
    scanf("%i     %i", &a, &b);

    if (a % b == 0)
        printf("a is evenly divisible by b\n");
    else
        printf("a is not divisible by b\n");
}