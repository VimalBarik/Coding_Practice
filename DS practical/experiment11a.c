#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct node {
    int year;
    char type[20];
    char company[20];
    struct node *left, *right;
};

struct node *newNode(int year, char type[], char company[]) {
    struct node *temp = (struct node *)malloc(sizeof(struct node));
    temp->year = year;
    strcpy(temp->type, type);
    strcpy(temp->company, company);
    temp->left = temp->right = NULL;
    return temp;
}

struct node *insert(struct node *root, int year, char type[], char company[]) {
    if (root == NULL) return newNode(year, type, company);
    if (year < root->year)
        root->left = insert(root->left, year, type, company);
    else if (year > root->year)
        root->right = insert(root->right, year, type, company);
    return root;
}

struct node *minValueNode(struct node *node) {
    struct node *current = node;
    while (current->left != NULL)
        current = current->left;
    return current;
}

struct node *deleteNode(struct node *root, int year) {
    if (root == NULL) return root;
    if (year < root->year)
        root->left = deleteNode(root->left, year);
    else if (year > root->year)
        root->right = deleteNode(root->right, year);
    else {
        if (root->left == NULL) {
            struct node *temp = root->right;
            free(root);
            return temp;
        }
        else if (root->right == NULL) {
            struct node *temp = root->left;
            free(root);
            return temp;
        }
        struct node *temp = minValueNode(root->right);
        root->year = temp->year;
        strcpy(root->type, temp->type);
        strcpy(root->company, temp->company);
        root->right = deleteNode(root->right, temp->year);
    }
    return root;
}

void inorder(struct node *root) {
    if (root != NULL) {
        inorder(root->left);
        printf("Year: %d\tType: %s\tCompany: %s\n", root->year, root->type, root->company);
        inorder(root->right);
    }
}

void preorder(struct node *root) {
    if (root != NULL) {
        printf("Year: %d\tType: %s\tCompany: %s\n", root->year, root->type, root->company);
        preorder(root->left);
        preorder(root->right);
    }
}

void postorder(struct node *root) {
    if (root != NULL) {
        postorder(root->left);
        postorder(root->right);
        printf("Year: %d\tType: %s\tCompany: %s\n", root->year, root->type, root->company);
    }
}

int main() {
    struct node *root = NULL;
    int choice, year;
    char type[20], company[20];
    while (1) {
        printf("\nBinary Search Tree Operations:\n");
        printf("1. Insert\n");
        printf("2. Delete\n");
        printf("3. Display (Inorder)\n");
        printf("4. Display (Preorder)\n");
        printf("5. Display (Postorder)\n");
        printf("6. Quit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        switch (choice) {
        case 1:
            printf("Enter year, type and company of the automobile: ");
            scanf("%d %s %s", &year, type, company);
            root = insert(root, year, type, company);
            break;
        case 2:
            printf("Enter year of the automobile to delete: ");
            scanf("%d", &year);
            root = deleteNode(root, year);
            break;
        case 3:
            printf("Inorder Traversal:\n");
            inorder(root);
            break;
        case 4:
            printf("Preorder Traversal:\n");
            preorder(root);
            break;
        case 5:
            printf("Postorder Traversal:\n");
            postorder(root);
            break;
        case 6:
            exit(0);
        default:
            printf("Wrong choice, please enter again\n");
        }
    }
    return 0;
}