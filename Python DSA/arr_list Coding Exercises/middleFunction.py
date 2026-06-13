# MY SOLUTION
# mylist = [1,2,3,4,5,6,7,8,9,10]
# def middle(lst):
#     lst.pop()
#     lst.pop(0)
#     return lst

# print(middle(mylist))


# COURSE SOLUTION
def middle(lst):
    return lst[1:-1]


mylist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(middle(mylist))
