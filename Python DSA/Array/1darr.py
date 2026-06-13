from array import *

my_array = array("i", [1,2,3,4,5])

#create array and traverse
for i in my_array:
    print(i)

# access individual elements through indexes
def accessElements(array, index):
    if index >= len(array):
        print("Index out of range")
    else:
        print(array[index])

accessElements(my_array, 2)

#append any value to the array using append() method
my_array.append(6)
print(my_array)

#insert value in an array using insert() method
my_array.insert(2,9)
print(my_array)

#extend python array using extend() method
my_array1 = array("i", [10,11,12])
my_array.extend(my_array1)
print(my_array)

#add items from list into array using fromlist() method
templist = [20, 21, 22]
my_array.fromlist(templist)
print(my_array)

#remove any array element using remove() method
my_array.remove(20)
print(my_array)

#remove last array element using pop() method
my_array.pop()
print(my_array)

#fetch any element through its index using index() method
print(my_array.index(21))

#reverse a python array using reverse() method
my_array.reverse()
print(my_array)

#get array buffer information through buffer_info() method
print(my_array.buffer_info())

#check for number of occurrances of an element using count() method
my_array.append(11)
print(my_array.count(11))

#convert array to string using tostring() method does not works in python 3.9 or later
# strtemp = my_array.tostring()
# print(strtemp)
# ints = array("i")
# ints.fromstring(strtemp)
# print(ints)

#convert array to a python list with same elements using tolist() method
print(my_array.tolist())

#slice elements from an array
print(my_array[:4])