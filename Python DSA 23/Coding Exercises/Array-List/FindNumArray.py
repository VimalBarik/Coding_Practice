import numpy as np

myArray = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])

def find_number(arr, num):
    for i in arr:
        if i == num:
            return "Number Found"
    return "Number Not Found"

print(find_number(myArray, 12))
