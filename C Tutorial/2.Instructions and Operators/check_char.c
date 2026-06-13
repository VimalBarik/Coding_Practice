#include<stdio.h>

int main()
{
   char x;
   printf("Enter the character: \n");
   scanf("%c", &x);

   printf("%i\n", x%1 != 0 );

}