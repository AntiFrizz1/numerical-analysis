import matplotlib.pyplot as plt
import math
import numpy

delta = 0.000001


def calculation(r, x):
    return r * x * (1 - x)


'''
def derivation(r, x):
    return r * (1 - 2 * x)
'''


def find_root_using_iterative_method(x0, r, n):
    x1 = x0
    table = [x0]

    for i in range(n):
        x0 = x1
        x1 = calculation(r, x0)
        table.append(x1)

    return x1, table


def get_x2(r):
    return 1 - 1 / r


def validate_r1(r1):
    i = 0.0
    step = 0.01

    while i < r1:
        x, table = find_root_using_iterative_method(0.9, i, 10000)
        i += step
        if math.fabs(x) > delta:
            return False

    return True


def is_monotone(array, ra):
    if len(array) < 3:
        return True

    sign = True if array[1] - array[2] <= delta else False

    for i in range(2, len(array) - 1):
        if (array[i] - array[i + 1] > delta) and sign:
            return False
        elif (array[i] - array[i + 1] < -delta) and (not sign):
            return False

    return True


def validate_r2(r1, r2):
    step = 0.01
    i = r1 + step

    while i < r2:
        x, table = find_root_using_iterative_method(0.9, i, 10000)
        if not (is_monotone(table, r2) and math.fabs(x - get_x2(i)) < delta):
            return False
        i += step

    return True


def validate_r3(r2, r3):
    step = 0.01
    i = r2 + step

    while i < r3:
        x, table = find_root_using_iterative_method(0.9, i, 10000)
        if not (math.fabs(x - get_x2(i)) < delta):
            return False
        i += step

    return True


def main():
    left = 0.0
    right = 50.0

    while right - left > delta:
        middle = (left + right) / 2.0

        if validate_r1(middle):
            left = middle
        else:
            right = middle

    r1 = (left + right) / 2.0
    print(r1)

    left = r1
    right = 50.0

    while right - left > delta:
        middle = (left + right) / 2.0

        if validate_r2(r1, middle):
            left = middle
        else:
            right = middle

    r2 = (left + right) / 2.0
    print(r2)

    left = r2
    right = 50.0

    while right - left > delta:
        middle = (left + right) / 2.0

        if validate_r3(r2, middle):
            left = middle
        else:
            right = middle

    r3 = (left + right) / 2.0
    print(r3)


def draw_plot_by_r(x0, r, n):
    x, table = find_root_using_iterative_method(x0, r, n)

    plt.plot(table)

    plt.show()
    plt.clf()


def draw_plot(r, x0):
    plt.axhline(color="black")
    plt.axvline(color="black")

    x = numpy.linspace(-1, 1, num=1000)

    plt.plot(x, r * x * (1 - x))

    x = numpy.linspace(-1, 1, num=10)

    plt.plot(x, x)

    x = [x0]
    y = [0]
    i = 0
    while i < 5:
        y0 = calculation(r, x0)
        x.append(x0)
        y.append(y0)
        y1 = y0
        x1 = y0
        x.append(x1)
        y.append(y1)
        if math.fabs(x0 - x1) < delta:
            break
        x0 = x1
        i += 1

    plt.plot(x, y)

    plt.show()
    plt.clf()


def draw_plot_lim_x_to_r():
    r = 0.0
    step_r = 0.05
    while r < 4:
        x = 0.8
        l_x, table = find_root_using_iterative_method(x, r, 10000)
        for i in table[9990:]:
            plt.scatter(r, i, c="green",s=2)
        r += step_r

    plt.show()
    plt.clf()

if __name__ == "__main__":
    #main()

    fig = plt.figure()

    #draw_plot_by_r(0.5, 0.5, 10)
    draw_plot(1.2, 0.2)
    #draw_plot_lim_x_to_r()

