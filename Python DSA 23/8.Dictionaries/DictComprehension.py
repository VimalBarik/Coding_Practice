import random

city_names = ["Paris", "London", "Rome", "Berlin", "Madrid"]

cityTemp = {city: random.randint(20,30) for city in city_names}
print(cityTemp)

above_25 = {city:temp for (city, temp) in cityTemp.items() if temp > 25}
print(above_25)
