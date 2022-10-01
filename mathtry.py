x = 0
n = True
for xP in range(20):
    if n is True:
        x = x + xP
        n = False
    else:
        x = x - xP
        n = True
    print(x)

