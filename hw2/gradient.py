from lib import *


def main():
    eps = 10 ** -9
    generated = random_matrix_generation()

    A, x, b, size = generated[0], generated[1], generated[2], generated[3]
    # A = [[2, 1], [0, 1]]
    # x = ['x0', 'x1']
    # b = [3, 1]
    # size = 2
    print("Generated values:")
    print_conditions(A, x, b)
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

    print("Результат для метода сопряженных градиентов:", approximations, "Количество шагов: {0}".format(steps), sep='\n')


if __name__ == "__main__":
    main()
