mydict = {'name': 'Edy', 'age': 26, 'address': 'London'}

def searchDict(dict, value):
    for key in dict:
        if dict[key] == value:
            return key, value

    return "The value does not exist"

print(searchDict(mydict, 26))