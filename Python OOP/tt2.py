class Employee:

    num_of_emps = 0
    raise_amount = 1.04
    def __init__(self, first, last, pay):
        self.first  = first
        self.last  = last
        self.pay  = pay
        self.email = first + "." +last +"@gmail.com"

        Employee.num_of_emps += 1

    def fullname(self):
        return f"{self.first} {self.last}"

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)

print(Employee.num_of_emps)

emp_1 = Employee("Vimal", "Barik", 50000)
emp_2 = Employee("Kanishk", "Rajput", 40000)

print(Employee.num_of_emps)