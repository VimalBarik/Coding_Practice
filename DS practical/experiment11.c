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
    root = insert(root, 2019, "Sedan", "Toyota");
    root = insert(root, 2020, "SUV", "Tesla");
    root = insert(root, 2018, "Coupe", "BMW");
    root = insert(root, 2022, "Truck", "Ford");

    printf("Inorder:\n");
    inorder(root);
    printf("\nPreorder:\n");
    preorder(root);
    printf("\nPostorder:\n");
    postorder(root);
    return 0;
}
