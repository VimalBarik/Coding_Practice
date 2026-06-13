def missing_number(arr, n):
    # TODO
    total = n*(n+1)//2
    arr_sum = sum(arr)
    return total - arr_sum
print(missing_number([1, 2, 3, 4, 6], 6))