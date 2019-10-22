import numpy as np
import lib


def explicit_euler_method(f, h, n, vec0, r, sigma=10, b=8 / 3):
    ans = []
    for i in range(len(vec0)):
        ans.append([])
    lib.transpose_and_add(ans, vec0)
    vec1 = vec0
    vec = [0] * len(vec0)
    for i in range(n):
        vec = lib.sum_vectors(vec1, lib.num_to_vector(h, f(vec1, sigma, b, r)))
        lib.transpose_and_add(ans, vec)
        vec1 = vec

    return ans


def not_explicit_euler_method(f, h, n, vec0, r, eps=0.0001, sigma=10, b=8 / 3):
    ans = []
    for i in range(len(vec0)):
        ans.append([])
    lib.transpose_and_add(ans, vec0)
    vec1 = vec0
    for i in range(n):
        vec_0 = lib.sum_vectors(vec1, lib.num_to_vector(h, f(vec1, sigma, b, r)))
        # vec_s = lib.sum_vectors(vec1, lib.num_to_vector(h, f(vec_0, sigma, b, r)))
        vec_s = lib.sum_vectors(vec1, lib.num_to_vector(h / 2.0, lib.sum_vectors(f(vec_0, sigma, b, r), f(vec1, sigma, b, r))))
        # while lib.euclidean_norm(lib.sub_vectors(vec_s, vec_0)) / lib.euclidean_norm(vec_0) > eps:
        #     vec_0 = vec_s
        #     vec_s = lib.sum_vectors(vec1, lib.num_to_vector(h, f(vec_0, sigma, b, r)))

        vec1 = vec_s
        lib.transpose_and_add(ans, vec1)

    return ans
