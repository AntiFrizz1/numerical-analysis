import math


def scalar_production(x, y):
    assert len(x) == len(y)

    ans = 0
    for i in range(len(x)):
        ans += x[i] * y[i]

    return ans


def num_to_vector(num, vec):
    ans = [0] * len(vec)
    for i in range(len(vec)):
        ans[i] = num * vec[i]

    return ans


def sum_vectors(x, y):
    assert len(x) == len(y)

    tmp = [0] * len(x)
    for i in range(len(x)):
        tmp[i] = x[i] + y[i]

    return tmp


def sub_vectors(x, y):
    assert len(x) == len(y)

    tmp = [0] * len(x)
    for i in range(len(x)):
        tmp[i] = x[i] - y[i]

    return tmp


def transpose_and_add(dest, src):
    assert len(dest) == len(src)

    for i in range(len(src)):
        dest[i].append(src[i])


def euclidean_norm(vec):
    ans = 0
    for i in range(len(vec)):
        ans += vec[i] ** 2
    return math.sqrt(ans)