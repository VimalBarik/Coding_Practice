def permutation(list1, list2):
    if len(list1) != len(list2):
        return False
    list1.sort()
    list2.sort()
    if list1 == list2:
        return True
    else:
        return False

list1 = ["a", "b", "c"]
list2 = ["c", "a", "b"]
print(permutation(list1, list2))