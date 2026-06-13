#include <stdio.h>

void bonjour();

void namaste();

int main()
{
    char ethnicity;

    printf("Enter I for indian and F for french\n");
    scanf("%c", &ethnicity);

    if (ethnicity == 'I')
    {
        namaste();
    }
    else if (ethnicity == 'F')
    {
        bonjour();
    }
    else
    {
        printf("Invalid input\n");
    }

    return 0;
}

void bonjour()
{
    printf("Bonjour\n");
    namaste();
}
void namaste()
{
    printf("Namaste\n");
}