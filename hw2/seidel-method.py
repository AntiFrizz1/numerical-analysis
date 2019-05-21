import lib

def prepare_system(matrix, vector):
    for i in range(len(matrix)):
        if (len(matrix) != len(matrix[i])) or matrix[i][i] == 0:
            raise RuntimeError('incorrect matrix: ' + matrix)

    if len(matrix) != len(vector):
        raise RuntimeError('incorrect matrix: ' + matrix + '. And vector: ' + vector)

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
    n = len(matrix)

    for i in range(n):
        vector = []
        for j in range(n):
            if i < j:
                vector.append(matrix[i][j])
                matrix[i][j] = 0
            else:
                vector.append(0)
        matrix1.append(vector)

    return matrix1


def seidel_method(matrix, vector, iterations):
    matrix1 = split_matrix(matrix)
    print(matrix)
    print(matrix1)
    n = len(matrix)

    answers = [0] * n
    for it in range(iterations):
        new_answers = [0] * n
        for i in range(n):
            new_answers[i] = lib.vector_on_vector(matrix[i], new_answers)\
                             + lib.vector_on_vector(matrix1[i], answers) + vector[i]
        answers = new_answers
        print(answers)

    return answers