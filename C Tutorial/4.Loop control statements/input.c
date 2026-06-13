#include <stdio.h>

int main()
{
    int n;
    /*for (int i = 0; i < 1000; i++)
    {
        printf("Enter Number: \n");
        scanf("%d", &n);

        if (n % 2 != 0)
        {
            break;
        }
    }*/

    do
    {
        printf("Enter Number: \n");
        scanf("%d", &n);
    } while (n % 7 != 0);
}