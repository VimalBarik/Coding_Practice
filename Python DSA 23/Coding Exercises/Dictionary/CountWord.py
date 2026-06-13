words = ['apple', 'orange', 'banana', 'apple', 'orange', 'apple']

print(words.count("apple"))
def count_word(words):
    myDict = {}
    for i in words:
        myDict[i] = words.count(i)
    return myDict

print(count_word(words))

