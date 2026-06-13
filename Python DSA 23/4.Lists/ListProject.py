days = int(input("How many day's tempearture?"))

temp_days = []
for i in range(days):
    temp_temp = input("Day "+str(i+1)+"'s high temp: ")
    temp_days.append(float(temp_temp))

average = sum(temp_days)/len(temp_days)
print("Average", average)
count = 0
for i in temp_days:
    if i > average:
        count += 1

print(str(count) +  "day(s) above average")
