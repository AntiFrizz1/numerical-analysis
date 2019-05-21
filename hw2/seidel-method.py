import lib


def prepare_system(matrix, vector):
    for i in range(len(matrix)):
        if matrix[i][i] == 0:
            raise RuntimeError('The matrix has zero on main diagonal')
        if len(matrix) != len(matrix[i]):
            raise RuntimeError('The matrix isn\'t square sized')

    if len(matrix) != len(vector):
        raise RuntimeError('Different size between matrix and vector')

    b_matrix = []
    c_vector = []

    n = len(matrix)

    for i in range(n):
        help_vector = []
        for j in range(n):
            if i == j:
                help_vector.append(0)
            else:
                help_vector.append(-matrix[i][j] / matrix[i][i])
        b_matrix.append(help_vector)

    for i in range(n):
        c_vector.append(vector[i] / matrix[i][i])

    return b_matrix, c_vector


def split_matrix(matrix):
    matrix1 = []
    matrix2 = []
    n = len(matrix)

    for i in range(n):
        vector1 = []
        vector2 = []
        for j in range(n):
            if i > j:
                vector1.append(matrix[i][j])
                vector2.append(0)
            else:
                vector1.append(0)
                vector2.append(matrix[i][j])
        matrix1.append(vector1)
        matrix2.append(vector2)

    return matrix1, matrix2


def seidel_method(matrix, vector, eps=1e-9):
    return seidel_method_with_relax(matrix, vector, eps, 1)


def seidel_method_with_relax(matrix, vector, eps=1e-9, w=0.9):
    matrix1, matrix2 = split_matrix(matrix)
    n = len(matrix)
    if lib.enorm(matrix1) + lib.enorm(matrix2) >= 1:
        raise RuntimeError("Algorithm can't work with this matrix")

    q = lib.enorm(matrix2) / (1 - lib.enorm(matrix1))

    answers = [0] * n

    f = True
    iterations = 0
    while f:
        new_answers = [0] * n
        iterations += 1
        for i in range(n):
            new_answers[i] = (1 - w) * answers[i] + w * lib.vector_on_vector(matrix1[i], new_answers) \
                             + w * lib.vector_on_vector(matrix2[i], answers) + w * vector[i]

        if lib.enorm(lib.subtract_vectors(new_answers, answers)) * q < eps:
            f = False
        answers = new_answers

    return answers, iterations


if __name__ == '__main__':
    A = lib.generate_conditional_matrix(5)
    b = lib.generate_vector(5)

    new_B, new_c = prepare_system(A, b)
    ans, it = seidel_method(new_B, new_c)
    print(ans, it)

    ans, it = seidel_method_with_relax(new_B, new_c)
    print(ans, it)
