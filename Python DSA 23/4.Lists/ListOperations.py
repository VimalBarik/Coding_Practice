a = [1,2,3]
b = [4,5,6]
c = a + b
print(c)
print(max(c))
print(min(c))
print(sum(c))
print(sum(c)/len(c))
d = [0,1]
d = d * 4
print(d)
print(len(d))


# total = 0
# count = 0
# while(True):
#     inp = input("Enter a number: ")
#     if inp == "Done":
#         break
#     value = float(inp)
#     total = total + value
#     count = count + 1
#     average = total/count

# print("Average", average)


mylist1 = []
while(True):
    inp = input("Enter a number: ")
    if inp == "Done":
        break
    value = float(inp)
    mylist1.append(value)
average = sum(mylist1)/len(mylist1)
print("Average", average)
