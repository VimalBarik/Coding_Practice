i = 42
f = 3.14
b = True
s = "hello"
lst = [1,2,3]
t = (4,5,6)
st = {7,8,9}
d = {"a" : 1}

for val in [i, f, b, s, lst, t, st, d]:
    print(type(val).__name__, "->", val)