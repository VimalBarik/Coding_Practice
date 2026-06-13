class Employee:
    def __init__(self, first, last, pay):
        self.first  = first
        self.last  = last
        self.pay  = pay
        self.email = first + "." +last +"@gmail.com"

    def fullname(self):
        return f"{self.first} {self.last}"

emp_1 = Employee("Vimal", "Barik", 50000)
emp_2 = Employee("Kanishk", "Rajput", 40000)

#print(emp_1)
#print(emp_2)


print(emp_1.email)
print(emp_2.email)

print(emp_1.fullname())
print(Employee.fullname(emp_2))

#print(emp_1.fullname())