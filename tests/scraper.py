def f(**kwargs):
    g(**kwargs)

def g(**kwargs):
    for k,v in kwargs.items():
        print(k,v)

d = {"more":"fuckers"}
f(fuck="you",mother="fucker",**d)