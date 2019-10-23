import math

def lorenz(vec, s, b, r):
    assert len(vec) == 3
    x = s * (vec[1] - vec[0])
    y = r * vec[0] - vec[1] - vec[0] * vec[2]
    z = vec[0] * vec[1] - b * vec[2]
    return [x, y, z]


def first_point():
    return [0, 0, 0]


def second_point(b, r):
    return [(b * (r - 1)) ** 0.5, (b * (r - 1)) ** 0.5, r - 1]


def third_point(b, r):
    return [-(b * (r - 1)) ** 0.5, -(b * (r - 1)) ** 0.5, r - 1]
