//Program to generate a table of triangular numbers .. Using nested for loops
#include<stdio.h>

int main(void){
    int n, m, number, triangularNumber, counter;
    printf("How many Number do you want to put?\n");
    scanf("%i", &m);
    for(counter=1; counter<=m; ++counter)
    {
        printf("What triangular number do you want?");
        scanf("%i", &number);

        triangularNumber = 0;

        for(n= 1; n <= number; ++n)
            triangularNumber +=n;
        printf("Triangular number %i is %i\n\n", number, triangularNumber);
        
    }
    return 0;
}