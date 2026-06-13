#include<stdio.h>

int main(){
    int n, count = 0;

    printf("Enter Number: ");
    scanf("%d", &n);

    for (int i = 1; i <= n; i++)
    {
        if(n%i == 0)
        {
            count++;
        }
    }
    if(count == 2)
    {
        printf("Its a prime number\n");
    }
    else {
        printf("Not a prime number\n");
    }
}