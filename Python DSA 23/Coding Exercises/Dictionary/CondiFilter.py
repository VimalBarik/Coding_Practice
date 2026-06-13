my_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# def filter_dict(my_dict, condition):
#     filtered_dict = {}
#     for key, value in my_dict.items():
#         if condition(key, value):
#             filtered_dict[key] = value
#         else:
#             continue
#     return filtered_dict

def filter_dict(my_dict, condition):
    return {k: v for k, v in my_dict.items() if condition(k, v)}

print(filter_dict(my_dict, lambda k, v: v % 2 == 0))
