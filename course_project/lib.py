import re
import math
import numpy

constants = dict()
constants['R'] = 8.314
constants['delta'] = 0.01


def read_constants():
    global constants
    f = open('constants.txt', 'r')
    head = re.split(R'\s+', f.readline().rstrip())
    unresolved = []
    for j in range(14):
        line = re.split(R'\s+', f.readline().rstrip())
        if len(line) == 1:
            break

        if len(line) != len(head):
            unresolved.append(line)
            continue

        tmp = dict()
        for i in range(1, len(head)):
            try:
                tmp[head[i]] = float(line[i])
            except ValueError:
                tmp[head[i]] = line[i]
        constants[line[0]] = tmp

    head.pop(13)
    head.pop(13)

    for j in range(len(unresolved)):
        tmp = dict()
        for i in range(1, len(head)):
            try:
                tmp[head[i]] = float(unresolved[j][i])
            except ValueError:
                tmp[head[i]] = unresolved[j][i]
        constants[unresolved[j][0]] = tmp

    for i in range(4):
        line = re.split(R'\s+', f.readline().rstrip())
        constants[line[0]] = {'densities': float(line[1])}

    f.close()


def phi(i, t):
    return constants[i]['f1'] + constants[i]['f2'] * math.log(x(t)) + constants[i]['f3'] / (x(t) ** 2) \
           + constants[i]['f4'] / x(t) + constants[i]['f5'] * x(t) + constants[i]['f6'] * (x(t) ** 2) \
           + constants[i]['f7'] * (x(t) ** 3)


def evaluate_constant(equation, t, pa):
    sum_g = 0
    p = 1

    for key in equation[0]:
        sum_g += gibbs(key, t) * equation[0][key]
        if constants[key]['Phase'] == 'g':
            p *= pa ** equation[0][key]

    for key in equation[1]:
        sum_g -= gibbs(key, t) * equation[1][key]
        if constants[key]['Phase'] == 'g':
            p /= pa ** equation[1][key]

    return math.exp(- sum_g / (constants['R'] * t)) * p


def x(t):
    return t / (10 ** 4)


def gibbs(i, t):
    return constants[i]['H(298)'] - phi(i, t) * t


def g(it, pe, t, pa, pg):
    return d(it, t, pa) * (pg[it] - pe[it]) / (constants['R'] * 1000 * t * constants['delta'])


def k(delta, t, pa):
    return math.exp(-delta / (constants['R'] * t)) / pa


def sigma(i):
    return (constants[i]['sigma'] + constants['N2']['sigma']) / 2


def eps(i):
    return math.sqrt(constants[i]['epsil'] * constants['N2']['epsil'])


def mu(i):
    return 2 * constants[i]['mu'] * constants['N2']['mu'] / (constants[i]['mu'] + constants['N2']['mu'])


def omega(i, t):
    return 1.074 * ((t / eps(i)) ** (-0.1604))


def d(i, t, pa):
    return 2.628 * (10 ** (-2)) * (t ** (3 / 2)) / (pa * sigma(i) * omega(i, t) * math.sqrt(mu(i)))


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


def scalar_dicts(dict1, dict2, arr):
    answer = dict()
    for i in range(len(arr)):
        answer[arr[i]] = dict1[arr[i]] * dict2[arr[i]]
    return answer


def sum_dicts(dict1, dict2, arr):
    answer = dict()
    for i in range(len(arr)):
        answer[arr[i]] = dict1[arr[i]] + dict2[arr[i]]
    return answer


def subtract_dicts(dict1, dict2, arr):
    answer = dict()
    for i in range(len(arr)):
        answer[arr[i]] = dict1[arr[i]] - dict2[arr[i]]
    return answer


def vector_to_dict(vector, arr):
    answer = dict()
    for i in range(len(arr)):
        answer[arr[i]] = vector[i]
    return answer


def dict_to_vector(dict1, arr):
    answer = []
    for i in arr:
        answer.append(dict1[i])
    return answer


def norm(a):
    return numpy.linalg.norm(a, ord=2)


def apply_vector(f1, pe, t, pa, pg):
    answer = []
    for i in f1:
        answer.append(i(pe, t, pa, pg))
    return answer


def apply_matrix(f1, pe, t, pa, pg):
    answer = []
    for i in range(len(f1)):
        answer.append(apply_vector(f1[i], pe, t, pa, pg))

    return answer


def check(vector1, vector2, eps):
    for i in range(len(vector1)):
        if abs(vector1[i] - vector2[i]) > eps:
            return False


    return True


def newton_method(elements, f, f_prime, x1, t, pa, pg, eps=1e-4):
    iterations = 0
    x2 = []
    while True:
        x2 = subtract_vectors(x1, matrix_on_vector(
            numpy.linalg.inv(apply_matrix(f_prime, x1, t, pa, pg)).tolist(), apply_vector(f, x1, t, pa, pg)))
        if norm(subtract_vectors(x2, x1)) < eps:
            break
        x1 = x2
        iterations += 1

    return vector_to_dict(x2, elements), iterations

