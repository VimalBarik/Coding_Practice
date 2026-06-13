mylist = ['a','b','c','d','e','f']
print(mylist[0:2])
mylist[0:2] = ['x','y']
print(mylist.pop())
del mylist[2:4]
mylist.remove('e')
print(mylist)
