import subprocess
import lib
import seidel_method
import gradient
import numpy


def generate_conditional_test():
    test = []

    for i in range(5, 11):
        test.append((lib.generate_conditional_matrix(i), lib.generate_vector(i)))

    for i in range(5):
        test.append((lib.generate_conditional_matrix(10), lib.generate_vector(10)))

    return test


def generate_random_test():
    test = []

    for i in range(5, 11):
        test.append((lib.generate_random_matrix(i), lib.generate_vector(i)))

    for i in range(5):
        test.append((lib.generate_random_matrix(10), lib.generate_vector(10)))

    return test


def generate_gilbert_test():
    test = []

    for i in range(5, 11):
        test.append((lib.generate_gilbert_matrix(i), lib.generate_vector(i)))

    return test


def test_gauss(test):
    answers = []
    for i in range(len(test)):
        (matrix, vector) = test[i]
        input_data = str(len(matrix)) + '\n'

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                input_data += str(matrix[i][j]) + ' '
            input_data += '\n'
        for i in range(len(vector)):
            input_data += str(vector[i]) + ' '
        # print(input_data)

        # ans = numpy.linalg.solve(matrix, vector).tolist()

        p = subprocess.Popen('echo \'' + input_data + '\' | ./gauss-system', shell=True, stdout=subprocess.PIPE)

        if p.returncode is None:
            str1 = p.stdout.read().decode('utf-8').rstrip()
            h = list(map(float, str1.split()))
            answers.append((h, -1))
        else:
            answers.append(([], -1))

        # ans1 = []
        # for i in range(len(ans)):
        #     ans1.append(str(ans[i]))
        # answers.append((ans1, -1))

    return answers


def test_jacobi(test, eps=1e-9):
    answers = []
    for i in range(len(test)):
        (matrix, vector) = test[i]
        input_data = str(len(matrix)) + '\n' + str(eps) + '\n'

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                input_data += str(matrix[i][j]) + ' '
            input_data += '\n'

        for i in range(len(vector)):
            input_data += str(vector[i]) + ' '

        file = open("input.txt", "w")
        print(input_data, file=file)
        file.close()

        p = subprocess.Popen('./jacobi < input.txt', shell=True, stdout=subprocess.PIPE)

        ans = p.stdout.read().decode('utf-8').split('\n')
        if len(ans) == 3:
            h = list(map(float, ans[0].rstrip().split()))
            answers.append((h, float(ans[1])))
        else:
            answers.append(([], -1))

    return answers


def test_seidel(test, eps=1e-9):
    answers = []
    for i in range(len(test)):
        (matrix, vector) = test[i]
        try:
            ans, it = seidel_method.seidel_method(matrix, vector, eps)
            answers.append((ans, it))
        except RuntimeError:
            answers.append(([], -1))

    return answers


def test_seidel_with_relax(test, eps=1e-9, w=1.1):
    answers = []
    for i in range(len(test)):
        (matrix, vector) = test[i]
        try:
            ans, it = seidel_method.seidel_method_with_relax(matrix, vector, eps, w)
            answers.append((ans, it))
        except RuntimeError:
            answers.append(([], -1))

    return answers


def test_gradient(test, eps=1e-9):
    answers = []
    for i in range(len(test)):
        (matrix, vector) = test[i]
        try:
            ans, it = gradient.run_gradient_method(matrix, vector, eps)
            answers.append((ans, it))
        except RuntimeError:
            answers.append(([], -1))

    return answers


def compile_cpp_file(filename):
    subprocess.Popen('c++ ' + filename + '.cpp -o ' + filename, shell=True, stdout=subprocess.PIPE)


def prepare_equantions(matrix, vector):
    max_size = 0
    n_m = []

    for i in range(len(matrix)):
        tmp = []
        for j in range(len(matrix[i])):
            str1 = str(matrix[i][j])
            tmp.append(str1)
            max_size = max(max_size, len(str1))
        tmp1 = str(vector[i])
        max_size = max(max_size, len(tmp1))
        tmp.append(tmp1)
        n_m.append(tmp)

    for i in range(len(n_m)):
        for j in range(len(n_m[i])):
            l = len(n_m[i][j])
            for k in range(0, max_size - l):
                n_m[i][j] += ' '

    return n_m


def prepare_vector(vector):
    max_size = 0
    tmp = []

    for i in range(len(vector)):
        str1 = str(vector[i])
        tmp.append(str1)
        max_size = max(max_size, len(str1))

    for i in range(len(tmp)):
        for k in range(0, max_size - len(tmp[i])):
            tmp[i] += ' '

    return tmp


def prepare_test(test, answers, file):

    report = []
    size1 = 0
    size2 = 0
    size3 = [0, 0, 0, 0, 0]

    for i in range(len(test)):
        (matrix, vector) = test[i]
        m = prepare_equantions(matrix, vector)
        cn = str(lib.condition_number(matrix))
        size2 = max(size2, len(cn))
        n_a = []
        for j in range(len(answers)):
            (ans, it) = answers[j][i]
            if len(ans) == 0:
                n_a.append("-")
                size3[j] = max(size3[j], 1)
            else:
                p = []
                for k in range(len(ans)):
                    p.append(str(ans[k]))

                str1 = " ".join(p)
                if it != -1:
                    str1 += " | " + str(it)
                n_a.append(str1)
                size3[j] = max(size3[j], len(str1))

        n_m = []
        for j in range(len(m)):
            str1 = " ".join(m[j])
            size1 = max(size1, len(str1))
            n_m.append(str1)

        report.append((n_m, cn, n_a))

    head = ["matrix", "cn", "gauss", "jacobi", "seidel", "seidel_relax", "gradient"]
    for i in range(0, size1 - 6):
        head[0] += ' '

    for i in range(0, size2 - 2):
        head[1] += ' '

    for i in range(0, size3[0] - 5):
        head[2] += ' '

    for i in range(0, size3[1] - 6):
        head[3] += ' '

    for i in range(0, size3[2] - 5):
        head[4] += ' '

    for i in range(0, size3[3] - 11):
        head[5] += ' '

    for i in range(0, size3[4] - 8):
        head[6] += ' '

    print(" ".join(head), file=file)

    for i in range(len(report)):
        (n_m, cn, n_a) = report[i]

        l = len(n_m[0])
        for j in range(0, size1 - l):
            n_m[0] += ' '

        print(n_m[0], end=' ', file=file)

        l = len(cn)
        for j in range(0, size2 - l):
            cn += ' '

        print(cn, end=' ', file=file)

        for j in range(len(n_a)):
            l = len(n_a[j])
            for k in range(0, size3[j] - l):
                n_a[j] += ' '

            print(n_a[j], end=' ', file=file)

        print(file=file)

        for j in range(1, len(n_m)):
            l = len(n_m[j])
            for k in range(0, size1 - l):
                n_m[j] += ' '

            print(n_m[j],file=file)

        print(file=file)


def run_test(eps=1e-9, w=1.5):
    compile_cpp_file("jacobi")
    compile_cpp_file("gauss-system")

    conditional_test = generate_gilbert_test()

    answ = [test_gauss(conditional_test), test_jacobi(conditional_test), test_seidel(conditional_test),
            test_seidel_with_relax(conditional_test), test_gradient(conditional_test)]
    file = open("conditional_test.txt", 'w')

    prepare_test(conditional_test, answ, file)

    file.close()


if __name__ == '__main__':
    run_test()
