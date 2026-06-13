# MY SOLUTION
# myList = [84,85,86,87,85,90,85,83,23,45,84,1,2,0]
# mylist2 = []

# def first_second(my_list):
#     for i in range(len(my_list)):
#         if my_list[i] in mylist2:
#             pass
#         else:
#             mylist2.append(my_list[i])

#     my_list = sorted(mylist2, reverse= True)
#     return f"{my_list[0]}, {my_list[1]}"

# print(first_second(myList))

# COURSE SOLUTION
def first_second(my_list):
    max1, max2 = float("-inf"), float("-inf")

    for num in my_list:
        if num > max1:
            max2 = max1
            max1 = num
        elif num > max2 and num != max1:
            max2 = num

    return max1, max2

my_list = [84, 85, 86, 87, 85, 90, 85, 83, 23, 45, 84, 1, 2, 0]
print(first_second(my_list))