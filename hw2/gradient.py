from lib import *


def run_gradient_method(A, b):
    eps = 10 ** -9
    size = len(b)

    approximations = [0] * size
    residuals = [i for i in b]
    direction = [i for i in b]
    steps = 0

    while True:
        steps += 1
        alpha = vector_on_vector(residuals, direction) / vector_on_vector(matrix_on_vector(A, direction), direction)
        tmp = num_on_vector(alpha, direction)
        for i in range(size):
            approximations[i] += tmp[i]

        tmp = num_on_vector(alpha, matrix_on_vector(A, direction))
        for i in range(size):
            residuals[i] -= tmp[i]

        if abs(max(residuals)) < eps:
            break

        betta = -vector_on_vector(matrix_on_vector(A, direction), residuals) \
                / vector_on_vector(matrix_on_vector(A, direction), direction)

        tmp = num_on_vector(betta, direction)
        for i in range(size):
            direction[i] = residuals[i] + tmp[i]

    # print("Результат для метода сопряженных градиентов:",
    #       *approximations,
    #       "Количество шагов: {0}".format(steps),
    #       sep='\n'
    #       )
    return approximations, steps


def main():
    A = generate_random_matrix(5)
    b = generate_vector(5)
    run_gradient_method(A, b)


if __name__ == "__main__":
    main()
