from array import *

def max_product(arr):
    max1 = 0
    max2 = 0
    for i in arr:
        if i > max1:
            max2 = max1
            max1 = i
        elif i > max2:
            max2 = i
    return max1*max2

my_arr = [1, 7, 3, 4, 9, 5]

print(max_product(my_arr))

