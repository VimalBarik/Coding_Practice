dict1 = {'a': 1, 'b': 2, 'c': 3}
dict2 = {'b': 3, 'c': 4, 'd': 5}


# def merge(dict1, dict2):
#     newDict = {}
#     for key in dict1:
#         newDict[key] = dict1[key] + dict2.get(key, 0)
#     for key in dict2:
#         if key not in newDict:
#             newDict[key] = dict2[key]
#     return newDict

def merge(dict1, dict2):
    result = dict1.copy()
    for key, value in dict2.items():
        result[key] = result.get(key, 0) + value
    return result

print(merge(dict1, dict2))
