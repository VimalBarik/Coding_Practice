myList = [84,85,86,87,85,90,85,83,23,45,84,1,2,0]

def second_best(arr):
    max1 = 0
    max2 = 0
    for i in arr:
        if i > max1:
            max2 = max1
            max1 = i
        elif i  > max2 and i == max1:
            max2 = i
    return max2

print(second_best(myList))
