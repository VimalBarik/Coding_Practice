import numpy as np

twoDarray = np.array([[11,15,10,6], [10,14,11,5], [12,17,12,8], [15,18,14,9]])
print(twoDarray)

def search2Darray(array, Value):
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] == Value:
                return "The value is located at index "+str(i)+" "+str(j)
    return "The element is not found"

print(search2Darray(twoDarray, 14))
