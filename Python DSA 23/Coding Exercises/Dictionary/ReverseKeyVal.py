my_dict = {'a': 1, 'b': 2, 'c': 3}

newDict = {}
# def reverse_dict(my_dict):
#     for key, value in my_dict.items():
#         newDict[value] = key
#     return newDict

def reverse_dict(my_dict):
    return {v: k for k, v in my_dict.items()}

print(reverse_dict(my_dict))
