# MY SOLUTION
# num_list = [2,6,3,9,11]
# sum_var = 9
# ravi_var = []
# for i in num_list:
#     if i < sum_var:
#         ravi_var.append(i)

# def two_sum(lists, sum):
#     for i  in lists:
#         for j in lists:
#             if i + j == sum:
#                 ans_list = [i,j]
#                 return ans_list

# print(two_sum(num_list, sum_var))

# COURSE SOLUTION
# def findPairs(nums, target):
#     for i in range(len(nums)):
#         for j in range(i+1, len(nums)):
#             if nums[i] == nums[j]:
#                 continue
#             elif nums[i] + nums[j] == target:
#                 print(i, j)

# myList = [1,2,3,2,3,4,5,6]
# findPairs(myList, 6)

#LEETCODE SOLUTION
def two_sum(nums, target):
    seen = {}

    for i, num in enumerate(nums):
        complement = target - num

        if complement in seen:
            return [seen[complement], i]

        seen[num] = i

nums = [2,7,11,15]
target = 9
indices = two_sum(nums, target)
print(f"Indices of the two numbers are: {indices}")