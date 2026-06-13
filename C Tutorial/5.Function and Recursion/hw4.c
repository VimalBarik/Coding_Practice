// Make your own pow function.
#include <stdio.h>

float power(float x, float y);

int main()
{
    float x, y;

    printf("Enter x:   ");
    scanf("%f", &x);

    printf("Enter y:  ");
    scanf("%f", &y);

    printf("%f", power(x, y));
    return 0;
}

float power(float x, float y)
{
    float t = x;
    for (int i = 1; i < y; i++)
    {
        x = x * t;
    }

    return x;
}
