#Update
mylist = [1,2,3,4,5,6,7]
print(mylist)
mylist[2] = 33
mylist[4] = 55
print(mylist)


#Insert
mylist1 = [1,2,3,4,5,6,7]
# print(mylist1)
mylist1.insert(0,11)
# print(mylist1)
mylist1.append(35)
print(mylist1)
newlist = [11,12,13,14]
mylist1.extend(newlist)
print(mylist1)
