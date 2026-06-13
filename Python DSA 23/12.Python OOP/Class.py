class Employee:
    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + "." + last + "@company.com"

    def fullname(self):
        return "{} {}".format(self.first, self.last)


emp_1 = Employee("vimal", "barik", 50000)
emp_2 = Employee("test", "user", 60000)

print(emp_1.fullname())
print(Employee.fullname(emp_1))
 
# print(emp_1)
# print(emp_2)

# emp_1.first = "Vimal"
# emp_1.last = "Barik"
# emp_1.email = "vimal.barik@company.com"
# emp_1.pay = 50000

# emp_2.first = "Test"
# emp_2.last = "User"
# emp_2.email = "test.user@company.com"
# emp_2.pay = 90000

print(emp_1.email)
print(emp_2.email)

print(emp_1.fullname())
