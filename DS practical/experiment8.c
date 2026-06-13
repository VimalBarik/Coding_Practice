#include <stdio.h>
#include <conio.h>
#include <malloc.h>
#include <string.h>

struct node
{
    int clg_id;
    char clg_name[100];
    struct node *next;
} *start;

int create_list(int clg_id, char clg_name[])
{
    struct node *new_node, *node;
    new_node = (struct node *)malloc(sizeof(struct node));
    new_node->clg_id = clg_id;
    strcpy(new_node->clg_name, clg_name);
    if (start == NULL)
    {
        new_node->next = new_node;
        start = new_node;
    }
    else
    {
        node = start;
        while (node->next != start)
            node = node->next;
        new_node->next = start;
        node->next = new_node;
    }
    return 0;
}
int display()
{
    struct node *node;
    if (start == NULL)
    {
        printf("\nList is empty ");
        return 0;
    }
    node = start;
    printf("\n \t College ID \t | \t Student Name ");
    do
    {
        printf(" \n \t %d \t \t \t %s ", node->clg_id, node->clg_name);
        node = node->next;
    } while (node != start);
    printf("\n");
    return 0;
}
int insert_at_beginning(int clg_id, char clg_name[])
{
    struct node *new_node, *node;
    new_node = (struct node *)malloc(sizeof(struct node));
    new_node->clg_id = clg_id;
    strcpy(new_node->clg_name, clg_name);
    node = start;
    while (node->next != start)s
        node = node->next;
    node->next = new_node;
    new_node->next = start;
    start = new_node;
    display();
    return 0;
}
int count()
{
    struct node *node = start;
    int count = 0;
    do
    {
        node = node->next;
        count++;
    } while (node != start);
    printf("\nNo. of records in the list are: %d\n", count);
    return 0;
}
int delete_from_end()
{
    struct node *node = start;
    if (node == NULL)
    {
        printf("\nUnderflow error ");
        return 0;
    }
    while (node->next->next != start)
    {
        node = node->next;
    }
    node->next = start;
    display();
    return 0;
}
int main()
{
    int ch, n, clg_id, i, pos;
    char clg_name[100];
    start = NULL;
    printf("Name:Angad Singh\tBranch:AI-Data Science\n");
    while (1)
    {
        printf("\n1. Create list");
        printf("\n2. Display link list");
        printf("\n3. Count number of elements in link list");
        printf("\n4. Insert at beginning in the list");
        printf("\n5. Delete from end of the list");
        printf("\n6. Quit");
        printf("\n\nEnter Choice : \t");
        scanf("%d", &ch);
        switch (ch)
        {
        case 1:
            printf("\nEnter no. of students : ");
            scanf("%d", &n);
            for (i = 1; i <= n; i++)
            {
                printf("\nEnter College ID : ");
                scanf("%d", &clg_id);
                printf("\nEnter name of Student : ");
                scanf("%s", &clg_name);
                create_list(clg_id, clg_name);
            }
            break;
        case 2:
            display();
            break;
        case 3:
            count();
            break;
        case 4:
            printf("\nEnter College ID : ");
            scanf("%d", &clg_id);
            printf("\nEnter name of Student : ");
            scanf("%s", &clg_name);
            insert_at_beginning(clg_id, clg_name);
            break;
        case 5:
            delete_from_end();
            break;
        case 6:
            exit(0);
        default:
            printf("\n Wrong Choice ");
        }
    }
    return 0;
}