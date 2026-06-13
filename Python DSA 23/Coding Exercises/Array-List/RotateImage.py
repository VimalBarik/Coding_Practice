# matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


# def rotate(matrix):
#     n = len(matrix)
#     ans = [[0] * n for num in range(n)]
#     for i in range(len(matrix)):
#         for j in range(len(matrix)):
#             ans[j][len(matrix) - 1 - i] = matrix[i][j]

#     return ans


# print(rotate(matrix))

# matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# def rotate(matrix):
#     for i in range(len(matrix)):
#         for j in range(i, len(matrix)):
#             matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
#     for i in range(len(matrix)):
#         matrix[i].reverse()

#     return matrix

# print(rotate(matrix))

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


def rotate(matrix):
    l, r = 0, len(matrix) - 1

    while l < r:
        for i in range(r - 1):
            top, bottom = l, r

            # save the topleft
            topleft = matrix[top][l + i]

            # move bottomleft into topleft
            matrix[top][l + i] = matrix[bottom - i][l]

            # move bottom right into bottom left
            matrix[bottom - i][l] = matrix[bottom][r - i]

            # move top right into bottom right
            matrix[bottom][r-i] = matrix[top+i][r]

            # move top left into top right
            matrix[top+i][r] = topleft
        r -= 1
        l += 1

rotate(matrix)
print(matrix)
