nums = [-1]

def maxSubArray(list):
    sum = 0
    maxSum = list[0]
    for i in range(len(list)):
        if sum < 0:
            sum = 0
        sum += list[i]
        maxSum = max(maxSum, sum)
    return maxSum

print(maxSubArray(nums))
