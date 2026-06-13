// Write a function to find square root of a number.
#include <stdio.h>

int root(int number);

int main()
{
    int number;

    printf("Enter Number:  ");
    scanf("%d", &number);

    printf("The Root is %d\n", root(number));
}

int root(int number)
{
    int root = 1;
    int square = 1;
    if (number == 1 || number == 0)
    {
        return number;
    }

    while (square < number)
    {
        root++;
        square = root * root;
    }
    return root;
}
