// Write a function to print "Hot" or "Cold" depending on the temperature user enters.
#include <stdio.h>

void thermo(int celsius);

int main()
{
    int celsius;
    printf("Enter temperature in celsius:  ");
    scanf("%d", &celsius);

    thermo(celsius);
}

void thermo(int celsius)
{
    if (celsius < 30)
    {
        printf("Cold\n");
    }
    else
    {
        printf("Hot\n");
    }
}