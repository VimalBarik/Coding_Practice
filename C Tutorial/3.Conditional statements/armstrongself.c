#include<stdio.h>

int main(void) {
    int n,r,sum=0,c;
    printf("Enter the number: \n");
    scanf("%d", &n);

    c= n;
    while(n>0)
    {
        r = n%10;
        sum = sum+(r*r*r);
        n=n/10;
    }
    if (c==sum)
    {
        printf("Armstrong Number\n");
    }
    else
    {
        printf("Not an armstrong number\n");
    }
return 0;

}