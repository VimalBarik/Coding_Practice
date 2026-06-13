#include <stdio.h>

int main()
{
    int count = 0;

    for (int i = 1; i <= 100; i++)
    {
        for (int j = 1; j <=100; j++)
        {
            if(j%i == 0)
            {
                count++;
            }
        }
        if(count == 2)
        {
            printf("%d", count);
        }
    }
}