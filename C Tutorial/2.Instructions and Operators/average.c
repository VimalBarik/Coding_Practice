#include<stdio.h>

int main(){
    int number1, number2, number3;
    printf("Enter Number 1: \n");
    scanf("%i", &number1);

    printf("Enter Number 2: \n");
    scanf("%i", &number2);

    printf("Enter Number 3: \n");
    scanf("%i", &number3);

    printf("Average: %.2f\n", (number1 + number2 + number3)/3.0);
}