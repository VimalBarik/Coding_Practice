my_list = [1,2,3,4,5]

def middle(lst):
    lst.pop(0)
    lst.pop()
    return lst
# print(middle(my_list))

def middle_1(lst):
    lst = lst[1:-1]
    return lst
print(middle_1(my_list))
