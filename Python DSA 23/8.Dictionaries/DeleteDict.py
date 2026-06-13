myDict = {'name': 'Edy', 'age': 27, 'address': 'London', "education": "Master"}

del myDict["age"]
removed_element = myDict.pop("educati", None)
myDict.popitem()
print(removed_element)
myDict.clear()
print(myDict)
