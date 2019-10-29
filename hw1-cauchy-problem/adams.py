import lib
import runge_kutta


def adams_method(f, h, n, vec0, r, sigma=10, b=8 / 3):
    ans = []
    for i in range(len(vec0)):
        ans.append([])
    lib.transpose_and_add(ans, vec0)
    vec_0 = vec0
    f0 = f(vec_0, sigma, b, r)
    vec_1_ = runge_kutta.runge_kutta(f, h, 1, vec_0, r, sigma, b)
    vec_1 = [vec_1_[0][0], vec_1_[1][0], vec_1_[2][0]]
    lib.transpose_and_add(ans, vec_1)
    f1 = f(vec_1, sigma, b, r)
    vec_2_ = runge_kutta.runge_kutta(f, h, 1, vec_1, r, sigma, b)
    vec_2 = [vec_2_[0][0], vec_2_[1][0], vec_2_[2][0]]
    lib.transpose_and_add(ans, vec_2)
    f2 = f(vec_2, sigma, b, r)
    vec_3_ = runge_kutta.runge_kutta(f, h, 1, vec_2, r, sigma, b)
    vec_3 = [vec_3_[0][0], vec_3_[1][0], vec_3_[2][0]]
    lib.transpose_and_add(ans, vec_3)
    f3 = f(vec_3, sigma, b, r)
    for i in range(n):
        vec_4_0 = lib.sum_vectors(vec_3,
                                lib.num_to_vector(h / 24,
                                                  lib.sum_vectors(lib.num_to_vector(55, f3),
                                                                  lib.sum_vectors(lib.num_to_vector(-59, f2),
                                                                                  lib.sum_vectors(lib.num_to_vector(37, f1),
                                                                                                  lib.num_to_vector(-9, f0)
                                                                                                  )
                                                                                  )
                                                                  )
                                                  )
                                )
        f_4_0 = f(vec_4_0, sigma, b, r)

        vec_4 = lib.sum_vectors(vec_3,
                                lib.num_to_vector(h / 24,
                                                  lib.sum_vectors(lib.num_to_vector(9, f_4_0),
                                                                  lib.sum_vectors(lib.num_to_vector(19, f3),
                                                                                  lib.sum_vectors(lib.num_to_vector(-5, f2),
                                                                                                  f1
                                                                                                  )
                                                                                  )
                                                                  )
                                                  )
                                 )
        f4 = f(vec_4, sigma, b, r)
        vec_0 = vec_1
        vec_1 = vec_2
        vec_2 = vec_3
        vec_3 = vec_4
        f0 = f1
        f1 = f2
        f2 = f3
        f3 = f4
        lib.transpose_and_add(ans, vec_4)

    return ans
