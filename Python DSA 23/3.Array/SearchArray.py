from array import *

arr1 = array("i", [1,2,3,4,5,6])

def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

print(linear_search(arr1, 4))
