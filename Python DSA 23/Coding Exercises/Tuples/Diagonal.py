input_tuple = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9)
)

def get_diagonal(input_tuple):
    diagonal = []
    for i in range(len(input_tuple)):
        for j in range(len(input_tuple[i])):
            if i == j:
                diagonal.append(input_tuple[i][j])
    return tuple(diagonal)

output_tuple = get_diagonal(input_tuple)
print(output_tuple)
