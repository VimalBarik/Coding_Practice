days = int(input("How many day's temperature? "))
temp_list = []
for i in range(days):
    temperature = int(input(f"Day {i + 1}'s temp: "))
    temp_list.append(temperature)

average = sum(temp_list)/len(temp_list)
print("Average = ", average)
new_list = [i for i in temp_list if i > average]
print(f"{len(new_list)} day(s) above average")
