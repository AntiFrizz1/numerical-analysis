import lib
import numpy
import matplotlib.pyplot as plt

def v_Al(g):
    return (g['AlCl'] + g['AlCl2'] + g['AlCl3']) * \
           (lib.constants['Al']['mu'] / lib.constants['Al(s)']['densities']) * 10 ** 9


def k1(t, pa):
    global equations
    return lib.evaluate_constant(equations[0], t, pa)


def k2(t, pa):
    global equations
    return lib.evaluate_constant(equations[1], t, pa)


def k3(t, pa):
    global equations
    return lib.evaluate_constant(equations[2], t, pa)


def run(t, pa, pg, eps=1e-4):
    global elements
    global f
    global f_prime

    x1 = [10, 10, 10, 10, 10]

    pe, iterations = lib.newton_method(elements, f, f_prime, x1, t, pa, pg, eps)
    g_dict = dict()

    for i in ['AlCl', 'AlCl2', 'AlCl3']:
        g_dict[i] = lib.g(i, pe, t, pa, pg)

    v = v_Al(g_dict)

    return g_dict, v


if __name__ == '__main__':
    equations = [
        [
            {
                'Al': 2,
                'HCl': 2
            },
            {
                'AlCl': 2,
                'H2': 1
            }
        ],
        [
            {
                'Al': 1,
                'HCl': 2
            },
            {
                'AlCl2': 1,
                'H2': 1
            }
        ],
        [
            {
                'Al': 2,
                'HCl': 6
            },
            {
                'AlCl3': 2,
                'H2': 3
            }
        ]
    ]
    lib.read_constants()

    elements = ['AlCl', 'AlCl2', 'AlCl3', 'HCl', 'H2']

    f = [
        lambda pe, t, pa, pg: -k1(t, pa) * (pe[0] ** 2) * pe[4] + (pe[3] ** 2),
        lambda pe, t, pa, pg: -k2(t, pa) * pe[1] * pe[4] + (pe[3] ** 2),
        lambda pe, t, pa, pg: -k3(t, pa) * (pe[2] ** 2) * (pe[4] ** 3) + (pe[3] ** 6),
        lambda pe, t, pa, pg: lib.d('HCl', t, pa) * (pg['HCl'] - pe[3]) + 2 * lib.d('H2', t, pa) * (pg['H2'] -
                                                                                                        pe[4]),
        lambda pe, t, pa, pg: lib.d('AlCl', t, pa) * (pg['AlCl'] - pe[0]) + 2 * lib.d('AlCl2', t, pa) * (
                pg['AlCl2'] - pe[1]) + 3 * lib.d('AlCl3', t, pa) * (pg['AlCl3'] - pe[2]) +
                              lib.d('HCl', t, pa) * (pg['HCl'] - pe[3])
    ]

    f_prime = [
        [
            lambda pe, t, pa, pg: -2.0 * k1(t, pa) * pe[0] * pe[4],
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: 2.0 * pe[3],
            lambda pe, t, pa, pg: -k1(t, pa) * (pe[0] ** 2)
        ],
        [
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: -k2(t, pa) * pe[4],
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: 2.0 * pe[3],
            lambda pe, t, pa, pg: -k2(t, pa) * pe[1]
        ],
        [
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: -2.0 * k3(t, pa) * pe[2] * (pe[4] ** 3),
            lambda pe, t, pa, pg: 6.0 * (pe[3] ** 5),
            lambda pe, t, pa, pg: -3.0 * k3(t, pa) * (pe[2] ** 2) * (pe[4] ** 2)
        ],
        [
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: -lib.d('HCl', t, pa),
            lambda pe, t, pa, pg: -2 * lib.d('H2', t, pa),
        ],
        [
            lambda pe, t, pa, pg: -lib.d('AlCl', t, pa),
            lambda pe, t, pa, pg: -2 * lib.d('AlCl2', t, pa),
            lambda pe, t, pa, pg: -3 * lib.d('AlCl3', t, pa),
            lambda pe, t, pa, pg: -lib.d('HCl', t, pa),
            lambda pe, t, pa, pg: 0
        ]
    ]

    pa1 = 100000
    pg1 = {
        'AlCl': 0,
        'AlCl2': 0,
        'AlCl3': 0,
        'HCl': 10000,
        'H2': 0,
    }

    t1 = 350 + 273.15
    t2 = 650 + 273.15
    eps = 0.0000001
    time = numpy.arange(1 / t2, 1 / t1, step=1e-5)

    answers = []
    for i in time:
        answers.append(run(1 / i, pa1, pg1, eps))

    v_e_Al = []
    g_AlCl = []
    g_AlCl2 = []
    g_AlCl3 = []
    for (g, v) in answers:
        v_e_Al.append(-v)
        g_AlCl.append(-g['AlCl'])
        g_AlCl2.append(-g['AlCl2'])
        g_AlCl3.append(-g['AlCl3'])

    plt.plot(time, g_AlCl, linestyle="--")
    plt.plot(time, g_AlCl2, linestyle="-")
    plt.plot(time, g_AlCl3, linestyle="-.")
    plt.legend((r'$-G_{AlCl}$', r'$-G_{AlCl_2}$', r'$-G_{AlCl_3}$'))
    plt.yscale('log')
    plt.xlabel(r'$T^{-1}, K^{-1}$')
    plt.ylabel(r'$-G_i, кмоль/(м^{2}*с)$')
    plt.grid(True)
    plt.show()

    plt.plot(time, v_e_Al)
    plt.yscale('log')
    plt.xlabel(r'$T^{-1}, K^{-1}$')
    plt.ylabel(r'$-V_{Al}, нм/с$')
    plt.grid(True)
    plt.show()
