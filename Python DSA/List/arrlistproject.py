high_temp = []
num_of_days = int(input("How many day's temperature? "))

for i in range(num_of_days):
    high_temp.append(int(input(f"Day {i + 1}'s high temp: ")))

total = sum(high_temp)
print(f"Average = {total/len(high_temp)}")

count = 0
for i in high_temp:
    if i > total / len(high_temp):
        count += 1
print(f"{count} day(s) above average")