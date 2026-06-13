from array import *

arr1 = array("i", [1,2,3,4,5,6])

def accessElement(array, index):
    if index  >= len(array):
        print("There is not any element in this index")
    else:
        print(array[index])

accessElement(arr1, 3)