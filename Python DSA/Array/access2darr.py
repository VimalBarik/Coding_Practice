import numpy as np

twoDarray = np.array([[11,15,10,6], [10,14,11,5], [12,17,12,8], [15,18,14,9]])
print(twoDarray)

def accessElements(array, rowIndex, colIndex):
    if rowIndex >= len(array) or colIndex >= len(array[0]):
        print("Incorrect Index")
    else:
        print(array[rowIndex][colIndex])

accessElements(twoDarray, 1, 2)