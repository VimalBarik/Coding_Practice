# integers = [1,2,3,4]
# print(integers)
# stringList = ["milk", "cheese", "butter"]
# print(stringList)
# mixList = [1, 1.5, "spam"]
# print(mixList)
# nestedList = []

# shoppingList = ["milk", "cheese","butter"]

# print(shoppingList[1])

# print("milk" in shoppingList)

# for i in shoppingList:
#     print(i)

# for i in range(len(shoppingList)):
#     shoppingList[i] = shoppingList[i]+"+"
#     print(shoppingList[i])

# myList = [1,2,3,4,5,6,7]
# print(myList)
# myList[2] = 33
# myList.insert(0,11)
# myList.append(55)
# newList = [11,12,13,14]
# myList.extend(newList)
# print(myList)
# myList = ["a", "b", "c", "d", "e", "f"]
# myList[0:2] = ["x", "y"]
# print(myList[:])
# print(myList.pop(2 ))
# del myList[0:2]
# myList.remove("e")
# print(myList )


# my_list = [10,20,30,40,50,60,70,80,90]
# target = 50
# if target in my_list:
#     print(f"{target} is in the list")
# else:
#     print(f"{target} is not in the list")
#linear search
# def linear_search(p_list, p_target):
#     for i, value in enumerate(p_list):
#         if value == p_target:
#             return i
#     return -1

# print(linear_search(my_list, target))


# a = [1,2,3]
# b = [4,5,6,7]
# c = a + b
# print(c)
# a = [0,1,2,3,4,5,6,7]
# a = a * 4
# print(len(a))
# print(max(a))
# print(min(a))
# print(sum(a))
# print(sum(a)/len(a))
# myList = list()
# while(True):
#     inp = input("Enter a number: ")
#     if inp == "done": break
#     value = float(inp)
#     myList.append(value)
# average = sum(myList)/len(myList)

# print("Average: ", average)


# a = "spam"
# a = "spam spam spam"
# b = list(a)
# b = a.split()
# print(b)
# a = "spam-spam1-spam2"
# delimiter = "-"
# b = a.split(delimiter)
# print(b)
# print(delimiter.join(b))


# prev_list = [1,2,3]
# new_list = [i*2 for i in prev_list]
# print(prev_list)
# print(new_list)
# language = "Python"
# new_list = [letter for letter in language]
# print(new_list)


# prev_list = [-1, 10, -20, 2, -90, 60, 45, 20]
# new_list = [number*number for number in prev_list if number < 0]
# print(new_list)
# sentence = "my name is vimal"
# def is_consonant(letter):
#     vowels = "aeiou"
#     return letter.isalpha() and letter.lower() not in vowels

# consonant = [i for i in sentence if is_consonant(i)]
# print(consonant)

prev_list = [-1, 10, -20, 2, -90, 60, 45, 20]
# new_list = [number if number > 0 else 0 for number in prev_list]
def get_number(number):
    if number > 0:
        return number
    else:
        return "negative number"

new_list = [get_number(number) for number in prev_list]
print(new_list)
