#include<stdio.h>

int main(){
    //Giving variable name to the number
    int n;

    //Prompting user for the number 
    printf("Enter the number: \n");
    scanf("%i", &n);

    //Calculating and printing the cube of the number
    printf("Cube of the number is %i\n", n*n*n);
}