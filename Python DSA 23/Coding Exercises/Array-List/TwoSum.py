def twoSum(nums,target):
    map = {}

    for i,n in enumerate(nums):
        diff = target - n
        if diff in map:
            return [map[diff], i]
        map[n] = i
    return
my_list = [2, 4, 3, 5, 6, -2, 4, 7, 8, 9]
print(twoSum(my_list, 9))
