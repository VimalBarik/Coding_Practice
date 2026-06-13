mylist = [1,2,3,4,5,6,7]
target = 6
if target in mylist:
    print(f"{target} is in the list")
else:
    print(f"{target} is not in the list")


def linear_search(p_list, p_target):
    for i, value in enumerate(p_list):
        if value == p_target:
            return i
    return "target not found"

print(linear_search(mylist, target))