list1 = [1, 2, 3, 2, 1]
list2 = [3, 1, 2, 1, 2]

# def check_sum_frequency(list1, list2):
#     dict1 = {}
#     dict2 = {}
#     for i in list1:
#         dict1[i] = list1.count(i)
#     for j in list2:
#         dict2[j] = list2.count(j)

#     if dict1 == dict2:
#         return True
#     return False

def check_same_frequency(list1, list2):
    def count_elements(lst):
        counter = {}
        for element in lst:
            counter[element] = counter.get(element, 0) + 1
        return counter

    return count_elements(list1) == count_elements(list2)

print(check_sum_frequency(list1, list2))
