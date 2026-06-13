# MY SOLUTION
# pairs = []
# index = []


# def pair_sum(mylist, sum):
#     for i in range(len(mylist)):
#         for j in range(len(mylist)):
#             if mylist[i] + mylist[j] == sum:
#                 if f"{i} + {j}" in index or f"{j} + {i}" in index:
#                     pass
#                 else:
#                     index.append(f"{i} + {j}")
#                     pairs.append(f"{mylist[i]} + {mylist[j]}")
#     return pairs


# print(pair_sum([2, 4, 3, 5, 6, -2, 4, 7, 8, 9], 7))


# COURSE SOLUTION
def pair_sum(arr, target_sum):
    result = []
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] + arr[j] == target_sum:
                result.append(f"{arr[i]}+{arr[j]}")
    return result

arr = [2, 4, 3, 5, 6, -2, 4, 7, 8, 9]
target_sum = 7
print(pair_sum(arr, target_sum))