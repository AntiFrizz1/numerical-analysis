import random
import numpy


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


def div_vector_on_num(num, vector):
    return [item / num for item in vector]


def sum_matrix(matrix1, matrix2):
    answer = []

    for i in range(len(matrix1)):
        vec = []
        for j in range(len(matrix1[i])):
            vec.append(matrix1[i][j] + matrix2[i][j])
        answer.append(vec)

    return answer


def subtract_vectors(vector1, vector2):
    answer = []
    for i in range(len(vector1)):
        answer.append(vector1[i] - vector2[i])

    return answer


def print_conditions(A, x, b):
    size = len(A)
    for i in range(size):
        row = ""
        for j in range(size - 1):
            row += "({0} * {1}) + ".format(str(A[i][j]), x[j])
        row += "({0} * {1}) = {2}".format(str(A[i][-1]), x[-1], str(b[i]))
        print(row)


def enorm(matrix):
    return numpy.linalg.norm(matrix, ord=2)


def condition_number(matrix):
    # matrix = numpy.array(matrix)
    return enorm(matrix) * enorm(numpy.linalg.inv(matrix))


def generate_conditional_matrix(size):
    matrix = numpy.eye(size, dtype=numpy.double) + numpy.random.normal(scale=0.1, size=(size, size))
    return (matrix @ matrix.T).tolist()


def generate_random_matrix(size):
    matrix = numpy.random.uniform(-1, 1, size=(size, size))
    return (matrix @ matrix.T).tolist()


def generate_gilbert_matrix(size):
    matrix = []
    for i in range(size):
        matrix.append([0] * size)

    for i in range(size):
        for j in range(size):
            matrix[i][j] = 1 / (1 + i + j)

    return matrix

