# MY SOLUTION
# unique = []
# def contains_duplicate(nums):
#     for i in nums:
#         if i in unique:
#             return True
#         else:
#             unique.append(i)
#     return False

# nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
# print(contains_duplicate(nums))

# COURSE SOLUTION
def contains_duplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(contains_duplicate(nums))