#include <stdio.h>

float percentage(float physics, float chemistry, float maths);

int main()
{
    float physics, chemistry, maths;
    printf("Enter  physics marks out of 100:  ");
    scanf("%f", &physics);

    printf("Enter chemistry marks out of 100:  ");
    scanf("%f", &chemistry);

    printf("Enter maths marks out of 100:  ");
    scanf("%f", &maths);

    printf("Percentage is %.2f\n", percentage(physics, chemistry, maths));
    return 0;
}
float percentage(float physics, float chemistry, float maths)
{
    float percent = (physics + maths + chemistry) / 3;
    return percent;
}
