import math
import matplotlib.pyplot as plt


def calculation(a):
    return a ** 3 - 5 * a ** 2 + 3 * a + 1


def derivation(a):
    return 3 * a ** 2 - 10 * a + 3


def find_min_and_max_abs_derivative_on_segment(left, right, step):
    max_value = math.fabs(derivation(left))
    min_value = math.fabs(derivation(left))

    local_x = left + step

    while local_x <= right:
        max_value = max(max_value, math.fabs(derivation(local_x)))
        min_value = min(min_value, math.fabs(derivation(local_x)))
        local_x += step

    return min_value, max_value


def find_root_using_iterative_method(left, right, eps):
    sign = 1
    if derivation((left + right) / 2.0) < 0:
        sign = -1

    min_value, max_value = find_min_and_max_abs_derivative_on_segment(left, right, 0.001)

    alpha = 2 / (max_value + min_value)
    q = (max_value - min_value) / (max_value + min_value)

    x0 = (left + right) / 2.0
    x1 = x0 - sign * alpha * calculation(x0)
    c = 0
    while math.fabs(x1 - x0) >= q / (1 - q) * eps:
        x0 = x1
        x1 = x0 - sign * alpha * calculation(x0)
        c += 1

    print(c)
    return x1


def localize_roots(left, right, step):
    table = []
    local = left

    while local - right <= 0:
        table.append((local, calculation(local)))
        local += step

    ans = []
    for j in range(0, len(table) - 1):
        if table[j][1] * table[j + 1][1] < 0:
            ans.append((table[j][0], table[j + 1][0]))

    return ans


def find_root_using_bisection_method(left, right, eps):
    local_left = left
    local_right = right

    f_left = calculation(local_left)
    c = 0
    while math.fabs(local_left - local_right) >= 2 * eps:
        c += 1
        middle = (local_left + local_right) / 2.0
        f_middle = calculation(middle)
        if f_left * f_middle <= 0:
            local_right = middle
        else:
            local_left = middle
            f_left = f_middle

    print(c)
    return (local_left + local_right) / 2.0


def find_root_using_newton_method(left, right, eps):
    x0 = (left + right) / 2
    x1 = x0 - calculation(x0) / derivation(x0)
    c = 0
    while x1 - x0 >= eps:
        x0 = x1
        x1 = x0 - calculation(x0) / derivation(x0)
        c += 1

    print(c)
    return x1


fig = plt.figure(num=None, figsize=(10, 6), dpi=100, facecolor='w', edgecolor='k')

x = []
y = []

i = -2.0
delta = 0.00001

plt.subplot(121)

while i <= 5.0:
    x.append(i)
    y.append(calculation(i))
    i += delta

plt.plot(x, y)

plt.axhline(color="black")
plt.axvline(color="black")

x = []
y = []

i = -2.0
delta = 0.001

plt.subplot(122)

while i <= 5.0:
    x.append(i)
    y.append(derivation(i))
    i += delta

plt.plot(x, y)

plt.axhline(color="black")
plt.axvline(color="black")

roots_local = localize_roots(-2, 0, 0.5)
print(roots_local)

delta = 0.000000000001

print("bisection method", find_root_using_bisection_method(roots_local[0][0], roots_local[0][1], delta))
print("iterative method", find_root_using_iterative_method(roots_local[0][0], roots_local[0][1], delta))
print("newton method", find_root_using_newton_method(roots_local[0][0], roots_local[0][1], delta))
plt.show()
