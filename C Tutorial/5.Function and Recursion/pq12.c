#include <stdio.h>

float converttemp(float celsius);

int main()
{
    float celsius;
    printf("Enter temp in C°:  ");
        scanf("%f", &celsius);

    printf("%f", converttemp(celsius));
    return 0;
}
float converttemp(float celsius)
{
    float far = celsius * (9.0/5.0) + 32;
    return far;
}