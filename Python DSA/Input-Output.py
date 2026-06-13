print("Hello", "world")
print("A", "B", "C", sep = "-")
print("no newline", end = " | ")
print("continues here")

name = "Bob"
score = 95.5
print(f"Name: {name}, Score: {score:.1f}")

print("Name: {}, Score: {:.2f}".format(name, score))

print("Name: %s, Score: %.2f" % (name, score))

simulated = "23"
age = int(simulated)
print(f"Next year you'll be {age + 1}")


