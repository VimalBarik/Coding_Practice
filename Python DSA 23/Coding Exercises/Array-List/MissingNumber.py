def missing_number(arr, n):
    # TODO
    result = n
    for i in range(1, n):
        result += (i - arr[i-1])
    return result
print(missing_number([1, 2, 3, 4, 6], 6))
