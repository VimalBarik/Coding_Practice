# MY SOLUTION
# myList2D= [[1,2,3],[4,5,6],[7,8,9]]
# diagonal = []

# def diagonal_sum(matrix):
#     for i in range(len(matrix)):
#         for j in range(len(matrix[0])):
#             if i == j:
#                 diagonal.append(matrix[i][j])
#             else:
#                 pass
#     return sum(diagonal)

# print(diagonal_sum(myList2D))

#COURSE SOLUTION
myList2D= [[1,2,3],[4,5,6],[7,8,9]]

def diagonal_sum(matrix):
    total = 0

    for i in range(len(matrix)):
        total += matrix[i][i]
    return total

print(diagonal_sum(myList2D))