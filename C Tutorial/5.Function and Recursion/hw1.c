//Write a function to find sum of digits of a number.
#include<stdio.h>

int sum(int a, int b);

int main(){

   int a, b;

   printf("Enter first number:   ");
   scanf("%d", &a);

   printf("Enter second number:   ");
   scanf("%d", &b);

   printf("The Sum is %d\n", sum(a, b));

   return 0;


}

int sum(int a, int b){
    int sum = a+b;
    return sum;
}