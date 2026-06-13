// Recurisve function
#include <stdio.h>

void printHW(float count);

int main()
{
    printHW(3.5);
    return 0;
}

void printHW(float count)
{
    if (count == 0)
    {
        return;
    }
    printf("Hello world\n");
    printHW(count - 1);
}