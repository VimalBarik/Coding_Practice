#include<stdio.h>

int main(){
    int n, sum;

    printf("Enter Number: \n");
    scanf("%d", &n);
    for (int i = 0; i < n; i++)
    {
        sum = sum + i;
        sum++;
    }
    printf("%d\n", sum);

}