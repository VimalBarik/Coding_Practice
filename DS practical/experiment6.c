//Linked list insertion at specific position in C
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
struct Node{
    int rollno;
    char name[100];
    int marks;
    struct Node *next;
};
// required for insertAfter
int getCurrSize(struct Node* node){
    int size=0;

    while(node!=NULL){
        node = node->next;
        size++;
    }
    return size;
}
//function to insert after nth node
void insertatNthNode(int n, int rollno,char *name,int marks, struct Node** head)
{
    int size = getCurrSize(*head);
    struct Node* newNode = (struct Node*) malloc(sizeof(struct Node));
    newNode->rollno = rollno;
    strcpy(newNode->name,name);
    newNode->marks=marks;
    newNode->next = NULL;
    // Can't insert if position to insert is greater than size of Linked List
    // can insert after negative pos
    if(n < 1 || n > size+1)
        printf("**Invalid position to insert**\n");
    // inserting first node
    else if(n == 0){
        newNode->next = *head;
        *head = newNode;
    }
    else
    {
        // temp used to traverse the Linked List
        struct Node* temp = *head;
        // traverse till the nth node
        while(--n>1)
            temp=temp->next;
        // assign newNode's next to nth node's next
        newNode->next= temp->next;
        // assign nth node's next to this new node
        temp->next = newNode;
        // newNode inserted b/w 3rd and 4th node
    }
}

void display(struct Node* node){
    // as linked list will end when Node is Null
    while(node!=NULL){
        printf("Rollno: %d \t Name: %s \t Marks: %d \n",node->rollno,node->name,node->marks);
        node = node->next;
    }
    printf("\n");
}
int main()
{
    //creating 4 pointers of type struct Node
    //So these can point to address of struct type variable
    printf("Name:Vimal \tBranch:AI-DS\n\n\n");

    struct Node* head = NULL;
    struct Node* node2 = NULL;
    // allocate 3 nodes in the heap
    head =  (struct Node*)malloc(sizeof(struct Node));
    node2 = (struct Node*)malloc(sizeof(struct Node));
    head->rollno = 1; // data set for head node
    strcpy(head->name,"Vimal"); // next pointer assigned to address of node2
    head->marks=95;
    head->next=node2;
    node2->rollno = 2;
    strcpy(node2->name,"Prakash");
    node2->marks=94;
    node2->next = NULL;
    printf("Current student record: \n");
    display(head);

    int ans;
    int rollno,marks,n;
    char name[100];
    do{
        printf("Enter you choice : \n");
        printf("1.Enter a record\n");
        printf("2.Display\n");
        printf("3.Exit\n");
        scanf("%d",&ans);
        switch (ans){
            case 1:
            printf("Enter the location : ");
            scanf("%d",&n);
            printf("Enter the roll no : ");
            scanf("%d",&rollno);
            printf("Enter the name : ");
            scanf("%s",name);
            printf("Enter the marks : ");
            scanf("%d",&marks);
            insertatNthNode(n,rollno,name,marks,&head);
            break;
            case 2:
            printf("Update recorded\n");
            display(head);
            break;
            case 3:
            exit(0);
            break;
        }
    }while (ans!=3);
    return 0;
}