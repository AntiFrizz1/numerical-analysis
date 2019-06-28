import lib
import numpy
import matplotlib.pyplot as plt

def v_Ga(g):
    return (g['GaCl'] + g['GaCl2'] + g['GaCl3']) * \
           (lib.constants['Ga']['mu'] / lib.constants['Ga(l)']['densities']) * 10 ** 9


def k4(t, pa):
    global equations
    return lib.evaluate_constant(equations[0], t, pa)


def k5(t, pa):
    global equations
    return lib.evaluate_constant(equations[1], t, pa)


def k6(t, pa):
    global equations
    return lib.evaluate_constant(equations[2], t, pa)


def run(t, pa, pg, epsil=1e-4):
    global elements
    global f
    global f_prime
    global x1

    pe, iterations = lib.newton_method(elements, f, f_prime, x1, t, pa, pg, epsil)
    g_dict = dict()

    x1 = lib.dict_to_vector(pe, elements)

    for i in ['GaCl', 'GaCl2', 'GaCl3']:
        g_dict[i] = lib.g(i, pe, t, pa, pg)

    v = v_Ga(g_dict)

    return g_dict, v


if __name__ == '__main__':
    equations = [
        [
            {
                'Ga': 2,
                'HCl': 2
            },
            {
                'GaCl': 2,
                'H2': 1
            }
        ],
        [
            {
                'Ga': 1,
                'HCl': 2
            },
            {
                'GaCl2': 1,
                'H2': 1
            }
        ],
        [
            {
                'Ga': 2,
                'HCl': 6
            },
            {
                'GaCl3': 2,
                'H2': 3
            }
        ]
    ]
    lib.read_constants()

    elements = ['GaCl', 'GaCl2', 'GaCl3', 'HCl', 'H2']

    f = [
        lambda pe, t, pa, pg: -k4(t, pa) * (pe[0] ** 2) * pe[4] + (pe[3] ** 2),
        lambda pe, t, pa, pg: -k5(t, pa) * pe[1] * pe[4] + (pe[3] ** 2),
        lambda pe, t, pa, pg: -k6(t, pa) * (pe[2] ** 2) * (pe[4] ** 3) + (pe[3] ** 6),
        lambda pe, t, pa, pg: lib.d('HCl', t, pa) * (pg['HCl'] - pe[3]) + 2 * lib.d('H2', t, pa) * (pg['H2'] - pe[4]),
        lambda pe, t, pa, pg: lib.d('GaCl', t, pa) * (pg['GaCl'] - pe[0]) + 2 * lib.d('GaCl2', t, pa) * (
                pg['GaCl2'] - pe[1]) + 3 * lib.d('GaCl3', t, pa) * (pg['GaCl3'] - pe[2]) + lib.d('HCl', t, pa) *
                              (pg['HCl'] - pe[3])
    ]

    f_prime = [
        [
            lambda pe, t, pa, pg: -2.0 * k4(t, pa) * pe[0] * pe[4],
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: 2.0 * pe[3],
            lambda pe, t, pa, pg: -k4(t, pa) * (pe[0] ** 2)
        ],
        [
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: -k5(t, pa) * pe[4],
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: 2.0 * pe[3],
            lambda pe, t, pa, pg: -k5(t, pa) * pe[1]
        ],
        [
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: -2.0 * k6(t, pa) * pe[2] * (pe[4] ** 3),
            lambda pe, t, pa, pg: 6.0 * (pe[3] ** 5),
            lambda pe, t, pa, pg: -3.0 * k6(t, pa) * (pe[2] ** 2) * (pe[4] ** 2)
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

    x1 = [0, 0, 1, 10, 10]

    pa1 = 100000
    pg1 = {
        'GaCl': 0,
        'GaCl2': 0,
        'GaCl3': 0,
        'HCl': 10000,
        'H2': 0,
    }

    t1 = 650 + 273.15
    t2 = 950 + 273.15
    eps = 0.00001
    time = numpy.arange(1 / t2, 1 / t1, step=1e-5)

    answers = []
    for i in time:
        answers.append(run(1 / i, pa1, pg1, eps))

    v_e_Ga = []
    g_GaCl = []
    g_GaCl2 = []
    g_GaCl3 = []
    for (g, v) in answers:
        v_e_Ga.append(-v)
        g_GaCl.append(-g['GaCl'])
        g_GaCl2.append(-g['GaCl2'])
        g_GaCl3.append(-g['GaCl3'])

    plt.plot(time, g_GaCl, linestyle="-")
    plt.plot(time, g_GaCl2, linestyle="--")
    plt.plot(time, g_GaCl3, linestyle="-.")
    plt.legend((r'$-G_{GaCl}$', r'$-G_{GaCl_2}$', r'$-G_{GaCl_3}$'))
    plt.xlabel(r'$T^{-1}, К^{-1}$')
    plt.ylabel(r'$-G_i, кмоль/(м^{2}*с)$')
    plt.yscale('log')
    plt.grid(True)
    plt.show()

    plt.plot(time, v_e_Ga)
    plt.xlabel(r'$T^{-1}, К^{-1}$')
    plt.ylabel(r'$-V_{Ga}, нм/с$')
    plt.yscale('log')
    plt.grid(True)
    plt.show()