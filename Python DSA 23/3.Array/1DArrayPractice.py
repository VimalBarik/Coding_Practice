from array import *
import numpy as np

#1.Create an array and traverse
print("Step1")
myarray = array("i", [1,2,3,4,5])
print(myarray)

myarray1 = np.array([1,2,3,4,5], dtype = int)
print(myarray1)

for i in myarray:
    print(i)

#2.Access individual elements through indexes
print("Step2")
def access_elements(arr, index):
    if index >= len(arr):
        print("Index does not exits")
    else:
        print(arr[index])

access_elements(myarray1, 3)

#3.Append any value to the array using append() method
print("Step3")
myarray.append(6)
print(myarray)

#4.Insert value in an array using insert() method
print("Step4")
myarray.insert(0, 11)
print(myarray)

#5. Extend python array using extend method
print("Step5")
myarray2 = array("i", [10,11,12,13,14])
myarray.extend(myarray2)
print(myarray)

#6.Add items from list into array using fromlist() method
print("Step6")
tempList = [20,21,22]
myarray.fromlist(tempList)
print(myarray)

#7.Remove any array element using remove() method
print("Step7")
myarray.remove(21)
print(myarray)

#8.Remove last array element using pop() method
print("Step8")
myarray.pop()
print(myarray)

#9.Fetch any element through its index using index() method
print("Step9")
print(myarray.index(20))

#10.Reverse a python array using reverse() method
print("Step10")
myarray.reverse()
print(myarray)

#11.Get array buffer information through buffer_info() method
print("Step11")
print(myarray.buffer_info())

#12.Check for number of occurances of an element using count() method
print("Step12")
myarray.append(11)
print(myarray.count(11))

#13.Convert an array to a python list with same elements using tolist() method
print("Step13")
print(myarray.tolist())

#14.Slice elememts from an array
print("Step16")
print(myarray[1:4])
