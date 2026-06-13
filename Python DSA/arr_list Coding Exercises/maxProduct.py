# COURSE SOLUTION
# def max_product(arr):
#     arr.sort(reverse = True)
#     return arr[0]*arr[1]

# arr = [1,7,3,4,9,5]
# print(max_product(arr))


# LEETCODE SOLUTION FROM COURSE
def max_product(arr):
    max1, max2 = 0, 0

    for num in arr:
        if num > max1:
            max2 = max1
            max1 = num

        elif num > max2:
            max2 = num
    return max1 * max2


arr = [1, 7, 3, 4, 9, 5]
print(max_product(arr))
