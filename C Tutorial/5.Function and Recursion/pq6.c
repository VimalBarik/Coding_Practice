#include<stdio.h>

void calculateprice(float value);

int main(){
    float value = 100.0;
    calculateprice(value);

printf("The value is %.2f\n", value);
return 0;

}

void calculateprice(float value){
    value = value + (value * 0.18);
    printf("Final price is %.2f\n", value);

}