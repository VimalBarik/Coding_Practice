// Function to calculate sum of two number
#include <stdio.h>

int sum(int a, int b);

int main()
{
    int a, b;

    printf("Enter a Number:  ");
    scanf("%d", &a);

    printf("Enter a Number:  ");
    scanf("%d", &b);

    

    printf("The sum is %d\n", sum(a, b));
}

int sum(int a, int b)
{
    return a + b;
}
