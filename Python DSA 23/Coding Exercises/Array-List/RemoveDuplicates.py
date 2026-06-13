my_list = [1, 1, 2, 2, 3, 4, 5]

def remove_duplicates(arr):
    my_list2 = []

    for i in arr:
        if i in my_list2:
            continue
        else:
            my_list2.append(i)
    return my_list2

print(remove_duplicates(my_list))
