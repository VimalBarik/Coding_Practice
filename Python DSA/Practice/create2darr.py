import numpy as np

twoDarray = np.array([[11,15,10,6], [10,14,11,5],[12, 17, 12, 8], [15, 18, 14, 9]])
print(twoDarray)

# newTwoDArray = np.insert(twoDarray, 0,  [[1,2,3,4]], axis=1)
# print(newTwoDArray)

# newTwoDArray = np.append(twoDarray, [[1,2,3,4]], axis=0)
# print(newTwoDArray)

# def accessElements(array, rowIndex, colIndex):
#     if rowIndex >= len(array) or colIndex >= len(array[0]):
#         print("Incorrect Index")
#     else:
#         print(array[rowIndex][colIndex])

# accessElements(twoDarray, 2, 3)

# def traverseTDArray(array):
#     for i in range(len(array)):
#         for j in range(len(array[0])):
#             print(array[i][j])

# traverseTDArray(twoDarray)

# def searchTDArray(array, value):
#     for i in range(len(array)):
#         for j in range(len(array[0])):
#             if array[i][j] == value:
#                 return "The value is located at index"+str(i)+" "+str(j)
#     return "The element is not found"

# print(searchTDArray(twoDarray, 14))

newTDarray = np.delete(twoDarray, 0, axis=0)
print(newTDarray)
