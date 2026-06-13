
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Global declaration
int count = 0;

// Structure declaration
struct node
{
    struct node *prev;
    int ssn;
    long long int phno;
    float sal;
    char name[20], dept[10], desg[20];
    struct node *next;
} *h, *temp, *temp1, *temp2, *temp4;

// Function to create node
void create()
{
    int ssn;
    long long int phno;
    float sal;
    char name[20], dept[10], desg[20];
    temp = (struct node *)malloc(sizeof(struct node));
    temp->prev = NULL;
    temp->next = NULL;
    printf("\n enter ssn, name, depart"
           "ment, designation, salary "
           "and phno of employee:\n");
    scanf("%d %s %s %s %f %lld",
          &ssn, name, dept, desg,
          &sal, &phno);
    temp->ssn = ssn;
    strcpy(temp->name, name);
    strcpy(temp->dept, dept);
    strcpy(temp->desg, desg);
    temp->sal = sal;
    temp->phno = phno;
    count++;
}

// Function to insert at beginning
void insertbeg()
{
    // If DLL is empty
    if (h == NULL)
    {
        create();
        h = temp;
        temp1 = h;
    }

    // Else create a new node and
    // update the links
    else
    {
        create();
        temp->next = h;
        h->prev = temp;
        h = temp;
    }
}

// Function to display from beginning
void displaybeg()
{
    temp2 = h;
    if (temp2 == NULL)
    {
        printf("\n list is empty\n");
        return;
    }
    printf("\n linked list elements "
           "from beginning:\n");
    while (temp2 != NULL)
    {
        printf("%d %s %s %s %f %lld\n",
               temp2->ssn, temp2->name,
               temp2->dept, temp2->desg,
               temp2->sal, temp2->phno);
        temp2 = temp2->next;
    }

    // Print the count
    printf("number of employees=%d", count);
}

// Function to delete at end
int deleteend()
{
    struct node *temp;
    temp = h;
    if (temp == NULL)
    {
        printf("list is empty\n");
        return 0;
    }
    if (temp->next == NULL)
    {
        printf("%d %s %s %s %f %lld\n",
               temp->ssn, temp->name,
               temp->dept, temp->desg,
               temp->sal, temp->phno);
        free(temp);
        h = NULL;
    }
    else
    {
        temp = temp1;
        temp2 = temp1->prev;
        temp2->next = NULL;
        printf("%d %s %s %s %f %lld\n",
               temp->ssn, temp->name,
               temp->dept, temp->desg,
               temp->sal, temp->phno);
        free(temp);
        temp1 = temp2;
    }
    count--;
    return 0;
}
// Function displaying menus
void employerDetails()
{
    int ch, n, i;
    h = NULL;
    temp = temp1 = NULL;
    printf("--------Menu------------\n");
    // printf("\n 1.create a DLL of n emp");
    printf("\n 1.display from beginning");
    printf("\n 2.delete at end");
    printf("\n 3.insert at beginning");
    printf("\n 4.exit\n");
    printf("----------------------\n");
    while (1)
    {
        printf("\n enter choice : ");
        scanf("%d", &ch);

        // Switch statements begins
        switch (ch)
        {
        /*case :
            printf("\n enter number of"
                   " employees:");
            scanf("%d", &n);
           // for (i = 0; i < n; i++)
             //   insertend();
            break;*/
        case 1:
            displaybeg();
            break;
        case 2:
            deleteend();
            break;
        case 3:
            insertbeg();
            break;
        case 4:
            exit(0);
        default:
            printf("wrong choice\n");
        }
    }
}

// Driver Code
int main()
{
    // Function Call
    employerDetails();

    return 0;
}
