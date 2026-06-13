# def missing_number(arr, n):
#     for i in range(0 ,len(arr) - 1):
#         if arr[i] + 1 == arr[i+1]:
#             continue
#         else:
#             print(arr[i] + 1)

# print(missing_number([1, 2, 3, 4, 6], 6))
# def findMissing(list, n):
#     sum1 = (n*(n+1))/2
#     sum2 = sum(list)
#     print(sum1 - sum2)

# mylist = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,19,20,21,22,23,24]
# findMissing(mylist, 24)


#twosum
# nums = [2, 7, 11,15]
# target = 9
# for i in range(0, len(nums)):
#     for j in range(i + 1, len(nums)):
#         if nums[i] + nums[j] == target:
#             print(i,j)
#         else:
#             continue
# def two_sum(nums, target):
#     seen = {}

#     for i, num in enumerate(nums):
#         complement = target - num

#         if complement in seen:
#             return [seen[complement], i]

#         seen[num] = i

# nums = [2,7, 11, 15]
# target = 9
# indices = two_sum(nums, target)
# print(f"Indices of the two numbers are: {indices}")


#finding a number in an array
# import numpy as np

# myarray = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])

# def findNumber(array, number):
#     for i in range(len(array)):
#         if array[i] == number:
#             print(i)

# findNumber(myarray, 13)


#max product
# def max_product(arr):
#     max1, max2 = 0, 0
#     for num in arr:
#         if num > max1:
#             max2 = max1
#             max1 = num
#         elif num > max2:
#             max2 = num
#     return max1*max2

# arr = [1,7,3,4,9,5]
# print(max_product(arr))


#middle function
# def middle(lst):
#     return lst[1:-1]

# my_list = [1,2,3,4]
# print(middle(my_list))


# Diagnonal Sum
# def diagonal_sum(matrix):
#     total = 0
#     for i in range(len(matrix)):
#         total += matrix[i][i]

#     return total

# myList2D= [[1,2,3],[4,5,6],[7,8,9]]
# print(diagonal_sum(myList2D))


#first, second best scores
# def first_second(mylist):
#     max1 =0
#     max2 =0
#     for num in mylist:
#         if num > max1:
#             max2 = max1
#             max1 = num
#         elif num > max2 and num != max1:
#             max2 = num
#     return max1, max2

# myList = [84,85,86,87,85,90,85,83,23,45,84,1,2,0]
# print(first_second(myList))


#duplicate number
# def remove_duplicates(lst):
#     mylist = []
#     for i in lst:
#         if i in mylist:
#             continue
#         else:
#             mylist.append(i)
#     return mylist

# my_list = [1,1,2,2,3,4,5]
# print(remove_duplicates(my_list))

# def remove_duplicates(lst):
#     unique_lst = []
#     seen = set()
#     for item in lst:
#         if item not in seen:
#             unique_lst.append(item)
#             seen.add(item)
#     return unique_lst

# my_list = [1,1,2,2,3,4,5]
# print(remove_duplicates(my_list))


#pairs
# def pair_sum(arr, target_sum):
#     result = []
#     for i in range(len(arr)):
#         for j in range(i+1, len(arr)):
#             if arr[i] + arr[j] == target_sum:
#                 result.append(f"{arr[i]}+{arr[j]}")
#     return result

# arr = [2,4,3,5,6,-2,4,7,8,9]
# target_sum = 7
# print(pair_sum(arr, target_sum))


#check duplicate
# def contains_duplicate(nums):
#     seen = set()
#     for num in nums:
#         if num in seen:
#             return True
#         seen.add(num)
#     return False

# nums = [1,2,3,4,5,6,7,8,9,1]
# print(contains_duplicate(nums))


#permutation
# def permutation(list1, list2):
#     if len(list1) != len(list2):
#         return False
#     list1.sort()
#     list2.sort()
#     if list1 == list2:
#         return True
#     else:
#         return False

# list1 = [1,2,3]
# list2 = [1,3,2]
# print(permutation(list1, list2))


#matrix rotation
# import numpy as np
# def rotate(matrix):
#     l,r = 0, len(matrix) - 1
#     while l < r:
#         for i in range(r - l):
#             top, bottom = l, r

#             #save the topleft
#             topLeft = matrix[top][l + i]

#             #move bottom left into top left
#             matrix[top][l + i] = matrix[bottom - i][l]

#             #move bottom right to bottom left
#             matrix[bottom - i][l] = matrix[bottom][r - i]

#             #move top right into bottom right
#             matrix[bottom][r - i] = matrix[top + i][r]

#             #move top left into top right
#             matrix[top + i][r] = topLeft
#         r -= 1
#         l += 1

# myMatrix = np.array([[1,2,3],[4,5,6],[7,8,9]])
# rotate(myMatrix)
# print(myMatrix)

#matrix rotation
import numpy as np
def rotate(matrix):
    n = len(matrix)

    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    for row in matrix:
        row[:] = row[::-1]

myMatrix = np.array([[1,2,3],[4,5,6],[7,8,9]])
rotate(myMatrix)
print(myMatrix)
