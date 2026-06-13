myList2D = [[1,2,3],[4,5,6],[7,8,9]]

def diagonal_sum(matrix):
    total_sum = 0
    for i in range(len(matrix)):
        total_sum += matrix[i][i]
    return total_sum

print(diagonal_sum(myList2D))
