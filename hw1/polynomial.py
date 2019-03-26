import math
import matplotlib.pyplot as plt


# class Polynomial:
#     a = []
#
#     def __init__(self, a1):
#         self.a = a1
#
#     def calculation(self, x):
#         ans = 0.0
#         local_x = 1.0
#
#         for i in range(0, len(self.a)):
#             ans += self.a[i] * local_x
#             local_x *= x
#
#         return ans
#
#     def localize_roots(self, left, right, step):
#         table = []
#         local = left
#
#         while local - right <= 0:
#             table.append((local, self.calculation(local)))
#             local += step
#
#         ans = []
#         for i in range(0, len(table) - 1):
#             if table[i][1] * table[i + 1][1] < 0:
#                 ans.append((table[i][0], table[i + 1][0]))
#
#         return ans
#
#     def find_root_using_bisection_method(self, left, right, delta):
#         local_left = left
#         local_right = right
#
#         f_left = self.calculation(local_left)
#
#         while math.fabs(local_left - local_right) >= 2 * delta:
#             middle = (local_left + local_right) / 2.0
#             f_middle = self.calculation(middle)
#             if f_left * f_middle <= 0:
#                 local_right = middle
#             else:
#                 local_left = middle
#                 f_left = f_middle
#
#         return (local_left + local_right) / 2.0
#
#     def derivation(self, x):
#         ans = 0.0
#         local_x = 1.0
#
#         for i in range(1, len(self.a)):
#             ans += i * self.a[i] * local_x
#             local_x *= x
#
#         return ans
#
#     def find_min_and_max_derivative_on_segment(self, left, right, step):
#         max_value = math.fabs(self.derivation(left))
#         min_value = math.fabs(self.derivation(left))
#
#         local_x = left + step
#
#         while local_x <= right:
#             max_value = max(max_value, math.fabs(self.derivation(local_x)))
#             min_value = min(min_value, math.fabs(self.derivation(local_x)))
#             local_x += step
#
#         return min_value, max_value
#
#     def revert(self):
#         for i in range(0, len(self.a)):
#             self.a[i] = -self.a[i]
#
#     def find_root_using_iterative_method(self, left, right, eps):
#         if self.derivation((left + right) / 2.0) < 0:
#             self.revert()
#
#         min_value, max_value = self.find_min_and_max_derivative_on_segment(left, right, eps)
#
#         if min_value == max_value:
#             alpha = 1 / max_value
#             q = 1 - min_value / max_value
#         else:
#             alpha = 2 / (max_value + min_value)
#             q = (max_value - min_value) / (max_value + min_value)
#
#         x0 = (left + right) / 2.0
#         x1 = x0 - alpha * self.calculation(x0)
#
#         while math.fabs(x1 - x0) >= (1 - q) / q * eps:
#             x0 = x1
#             x1 = x0 - alpha * self.calculation(x0)
#
#         return x1
#
#     def find_root_using_newton_method(self, left, right, eps):
#         x0 = (left + right) / 2
#         x1 = x0 - self.calculation(x0) / self.derivation(x0)
#
#         while x1 - x0 >= eps:
#             x0 = x1
#             x1 = x0 - self.calculation(x0) / self.derivation(x0)
#
#         return x1
#
#
# def first():
#     a = list(map(int, input().split()))
#     polynomial = Polynomial(a)
#     a, b = polynomial.localize_roots(-3, 2, 0.001)[0]
#     print(polynomial.find_root_using_bisection_method(a, b, 0.0000001))
#     print(polynomial.find_root_using_newton_method(a, b, 0.0000001))
#     print(polynomial.find_root_using_iterative_method(a, b, 0.0000001))


def calculation(x):
    return x ** 3 - 5 * x ** 2 + 3 * x + 5


def derivation(x):
    return 3 * x ** 2 - 10 * x + 3


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

    min_value, max_value = find_min_and_max_abs_derivative_on_segment(left, right, eps)

    if min_value == max_value:
        alpha = 1 / max_value
        q = 1 - min_value / max_value
    else:
        alpha = 2 / (max_value + min_value)
        q = (max_value - min_value) / (max_value + min_value)

    x0 = (left + right) / 2.0
    x1 = x0 -  sign * alpha * calculation(x0)

    while math.fabs(x1 - x0) >= (1 - q) / q * eps:
        x0 = x1
        x1 = x0 - sign * alpha * calculation(x0)

    return x1


def localize_roots(left, right, step):
    table = []
    local = left

    while local - right <= 0:
        table.append((local, calculation(local)))
        local += step

    ans = []
    for i in range(0, len(table) - 1):
        if table[i][1] * table[i + 1][1] < 0:
            ans.append((table[i][0], table[i + 1][0]))

    return ans


def find_root_using_bisection_method(left, right, delta):
    local_left = left
    local_right = right

    f_left = calculation(local_left)

    while math.fabs(local_left - local_right) >= 2 * delta:
        middle = (local_left + local_right) / 2.0
        f_middle = calculation(middle)
        if f_left * f_middle <= 0:
            local_right = middle
        else:
            local_left = middle
            f_left = f_middle

    return (local_left + local_right) / 2.0


def find_root_using_newton_method(left, right, eps):
    x0 = (left + right) / 2
    x1 = x0 - calculation(x0) / derivation(x0)

    while x1 - x0 >= eps:
        x0 = x1
        x1 = x0 - calculation(x0) / derivation(x0)

    return x1


fig = plt.figure()

x = []
y = []

i = -2.0
delta = 0.001

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

roots_local = localize_roots(-2, 0, 0.1)
print(roots_local)

print("bisection method", find_root_using_bisection_method(roots_local[0][0], roots_local[0][1], 0.000001))
print("iterative method", find_root_using_iterative_method(roots_local[0][0], roots_local[0][1], 0.000001))
print("newton method", find_root_using_newton_method(roots_local[0][0], roots_local[0][1], 0.000001))
plt.show()
