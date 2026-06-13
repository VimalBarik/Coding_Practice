my_list = [2, 4, 3, 5, 6, -2, 4, 7, 8, 9]

def pairs(list, target):
    list2 = []
    for i in range(len(list)):
        for j in range(i+1, len(list)):
            if list[i] + list[j] == target:
                list2.append(f"({list[i]}+{list[j]})")
            else:
                continue
    return list2

print(pairs(my_list, 7))

