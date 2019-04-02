import matplotlib.pyplot as plt


def calculation(x):
    return pow(x, 3) - 1


def derivation(x):
    return 3 * pow(x, 2)


def find_root_using_newton_method(x0, eps):
    x1 = x0 - calculation(x0) / derivation(x0)

    while abs(x1 - x0) >= eps:
        x0 = x1
        x1 = x0 - calculation(x0) / derivation(x0)

    return x1


xa = []
ya = []
ca = []


def add_point(x):
    point = find_root_using_newton_method(x, 0.001)
    xa.append(x.real)
    ya.append(x.imag)
    if (point.real < 0) and (point.imag > 0):
        color = "green"
    elif (point.real < 0) and (point.imag < 0):
        color = "red"
    else:
        color = "blue"
    ca.append(color)


fig = plt.figure(num=None, figsize=(10, 10), dpi=100, facecolor='w', edgecolor='k')

delta = 0.01

i = -2.0
while i <= 2.0:
    j = -2.0
    while j <= 2.0:
        add_point(complex(i, j))
        j += delta
    i += delta
plt.scatter(xa, ya, c=ca, s=1.5)

plt.show()
