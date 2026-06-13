prevList = [-1, 10, -20, 2, -90, 60, 45, 20]
newList = [number*number for number in prevList if number < 0]
print(newList)

sentence = "My name is Vimal"

def is_consonant(letter):
    vowels = "aeiou"
    return letter.isalpha() and letter.lower() not in vowels

consonants = [i for i in sentence if is_consonant(i)]
print(consonants)

# prevList = [-1, 10, -20, 2, -90, 60, 45, 20]
# new_list = [number if number > 0 else "Negative Number" for number in prevList]
# print(new_list)

def get_number(number):
    if number > 0:
        return number
    else:
        return "Negative Number"

prev_list = [-1, 10, -20, 2, -90, 60, 45, 20]
new_list = [get_number(number) for number in prev_list]
print(new_list)
