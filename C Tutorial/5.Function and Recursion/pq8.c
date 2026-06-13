#include <stdio.h>

float circleArea(float rad);
float squareArea(float side);
float rectangleArea(float a, float b);

int main()
{
    int a, b, side, rad;
    a = 5.0;
    b = 10.0;
    rad = 3;
    side = 3;

    printf("Area of rectangle is %f\n", rectangleArea(a, b));
    printf("Area of square is %f\n", squareArea(side));
    printf("Area of circle is %f\n", circleArea(rad));

    return 0;
}

float circleArea(float rad)
{
    return 3.14 * rad * rad;
}

float squareArea(float side)
{
    return side * side;
}
float rectangleArea(float a, float b)
{
    return a * b;
}
