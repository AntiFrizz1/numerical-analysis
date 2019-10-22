import lib


def runge_kutta(f, h, n, vec0, r, sigma=10, b=8 / 3):
    ans = []
    for i in range(len(vec0)):
        ans.append([])
    lib.transpose_and_add(ans, vec0)
    vec1 = vec0

    for i in range(n):
        k1 = f(vec1, sigma, b, r)
        k2 = f(lib.sum_vectors(vec1, lib.num_to_vector(h / 2, k1)), sigma, b, r)
        k3 = f(lib.sum_vectors(vec1, lib.num_to_vector(h / 2, k2)), sigma, b, r)
        k4 = f(lib.sum_vectors(vec1, lib.num_to_vector(h, k3)), sigma, b, r)
        vec = lib.sum_vectors(vec1, lib.num_to_vector(h / 6,
                                                      lib.sum_vectors(k1,
                                                                      lib.sum_vectors(lib.num_to_vector(2, k2),
                                                                                      lib.sum_vectors(lib.num_to_vector(2, k3),
                                                                                                      k4
                                                                                                      )
                                                                                      )
                                                                      )
                                                      )
                              )
        vec1 = vec
        lib.transpose_and_add(ans, vec1)

    return ans