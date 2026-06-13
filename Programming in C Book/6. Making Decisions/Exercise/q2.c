#include <stdio.h>

int main(void)
{
    float a, b;

    printf("Enter two number:  \n");
    scanf("%f%f", &a, &b);

    if (b == 0)
        printf("Division by zero\n");
    else
        printf("%.3f\n", a / b);

    return 0;
}