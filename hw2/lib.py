import random


def random_matrix_generation():
    size = random.randint(2, 4)

    A = []
    x = []
    b = []

    for i in range(size):
        A.append([random.randint(-10, 10) for j in range(size)])

    for i in range(size):
        x.append("x{0}".format(i))

    for i in range(size):
        b.append(random.randint(-10, 10))

    return A, x, b, size


def matrix_on_vector(matrix, vector):
    ans = []

    for i in range(len(matrix)):
        cur = 0
        for j in range(len(matrix[i])):
            cur += matrix[i][j] * vector[j]
        ans.append(cur)

    return ans


def vector_on_vector(first, second):
    ans = 0
    for i in range(len(first)):
        ans += first[i] * second[i]
    return ans


def num_on_vector(num, vector):
    return [num * item for item in vector]


def print_conditions(A, x, b):
    size = len(A)
    for i in range(size):
        row = ""
        for j in range(size - 1):
            row += "({0} * {1}) + ".format(str(A[i][j]), x[j])
        row += "({0} * {1}) = {2}".format(str(A[i][-1]), x[-1], str(b[i]))
        print(row)