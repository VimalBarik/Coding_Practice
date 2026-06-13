tuple1 = (1, 2, 3, 4, 5)
tuple2 = (4, 5, 6, 7, 8)

def common_elements(tuple1, tuple2):
    common_elements = []
    for i in tuple1:
        for j in tuple2:
            if i == j:
                common_elements.append(i)
            else:
                continue
    return tuple(common_elements)

print(common_elements(tuple1, tuple2))
