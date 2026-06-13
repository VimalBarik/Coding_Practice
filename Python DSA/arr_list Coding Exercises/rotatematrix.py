# MY INCOMPLETE SOLUTION
# matrix = [[1,2,3],[4,5,6],[7,8,9]]

# def rotate(matrix):
#     for j in range(len(matrix[0])):
#         for i in range(len(matrix) - 1, -1, -1):

#     return matrix


# print(rotate(matrix))

# NEETCODE SOLUTION
# def rotate(matrix):
#     l, r = 0, len(matrix) - 1

#     while l < r:
#         for i in range(r - l):
#             top, bottom = l, r

#             # Save the topleft
#             topleft = matrix[top][l + i]

#             # Move bottom left into top left
#             matrix[top][l + i] = matrix[bottom - i][l]

#             # Move bottom right into bottom left
#             matrix[bottom - i][l] = matrix[bottom][r - i]

#             # Move top right into bottom right
#             matrix[bottom][r - i] = matrix[top + i][r]

#             # Move top left into top right
#             matrix[top + i][r] = topleft

#         r -= 1
#         l += 1
#     return matrix

# matrix = [[1,2,3],[4,5,6],[7,8,9]]

# print(rotate(matrix))


# COURSE SOLUTION
def rotate(matrix):
    n = len(matrix)

    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    for row in matrix:
        row.reverse()

    return matrix

matrix = [[1,2,3],[4,5,6],[7,8,9]]

print(rotate(matrix))