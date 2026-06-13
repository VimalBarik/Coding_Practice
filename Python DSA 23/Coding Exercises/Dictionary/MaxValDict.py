my_dict = {'a': 5, 'b': 9, 'c': 2}

# def max_value_key(my_dict):
#     max = float("-inf")
#     max2 = None
#     for key, value in my_dict.items():
#         if value > max:
#             max = value
#             max2 = key
#         else:
#             continue
#     return max2

def max_value_key(my_dict):
    return max(my_dict, key=my_dict.get)

print(max_value_key(my_dict))

