mylist = []
while(True):
    inp = input("Enter a number")
    if inp == "done":
        break
    mylist.append(float(inp))

average = sum(mylist)/len(mylist)
print(average)
