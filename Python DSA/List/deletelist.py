mylist = [1,2,3,4,5,6,7,8,9]
mylist[0:2] = [11,12]
print(mylist)
mylist.pop(0)
print(mylist)
del mylist[3:5]
print(mylist)
mylist.remove(9)
print(mylist)