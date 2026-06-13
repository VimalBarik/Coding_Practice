#include<stdio.h>

int main(){
    //giving variable names to the sides
    int side_a, side_b;

    //prompting user for the side a
    printf("Enter Side 1: \n");
    scanf("%i", &side_a);

    //Prompting user for the side b
    printf("Enter Side 2: \n");
    scanf("%i", &side_b);

    //calculating and printing the perimeter of the rectangle
    printf("Perimeter of the rectangle %i\n", 2*(side_a + side_b));
}