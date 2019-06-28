import lib
import numpy
import matplotlib.pyplot as plt


def v_AlGaN(g):
    return (g['AlCl3'] * (lib.constants['AlN']['mu'] / lib.constants['AlN(s)']['densities']) +
            g['GaCl'] * (lib.constants['GaN']['mu'] / lib.constants['GaN(s)']['densities'])) * (10 ** 9)


def k9(t, pa):
    global equations
    return lib.evaluate_constant(equations[0], t, pa)


def k10(t, pa):
    global equations
    return lib.evaluate_constant(equations[1], t, pa)


def run(mode, xg, pa, pg1, epsil=1e-4):
    global elements
    global f
    global f_prime
    global t
    global x1

    pg1['AlCl3'] = xg * 30
    pg1['GaCl'] = 30 - pg1['AlCl3']
    if mode == 1:
        pg1['H2'] = 0
        pg1['N2'] = 98470
    else:
        pg1['H2'] = 9847
        pg1['N2'] = 88623
    pe, iterations = lib.newton_method(elements, f, f_prime, x1, t, pa, pg1, epsil)
    x1 = lib.dict_to_vector(pe, elements)
    g_dict = dict()
    print(pe)
    print(pg1)
    for i in ['GaCl', 'AlCl3']:
        g_dict[i] = lib.g(i, pe, t, pa, pg1)

    v = v_AlGaN(g_dict)
    print("x: " + str(xg) + " " + str(g_dict) + " " + str(v))
    return g_dict, v, pe['x']


if __name__ == '__main__':
    x1 = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

    equations = [
        [
            {
                'AlCl3': 1,
                'NH3': 1
            },
            {
                'AlN': 1,
                'HCl': 3
            }
        ],
        [
            {
                'GaCl': 1,
                'NH3': 1
            },
            {
                'GaN': 1,
                'HCl': 1,
                'H2': 1
            }
        ]
    ]
    lib.read_constants()
    elements = ['AlCl3', 'GaCl', 'NH3', 'HCl', 'H2', 'x']

    f = [
        lambda pe, t, pa, pg: -k9(t, pa) * pe[5] * (pe[3] ** 3) + pe[0] * pe[2],
        lambda pe, t, pa, pg: -k10(t, pa) * (1 - pe[5]) * pe[3] * pe[4] + pe[1] * pe[2],
        lambda pe, t, pa, pg: lib.d('HCl', t, pa) * (pg['HCl'] - pe[3]) + 2 * lib.d('H2', t, pa) * (pg['H2'] - pe[4])
                              + 3 * lib.d('NH3', t, pa) * (pg['NH3'] - pe[2]),
        lambda pe, t, pa, pg: 3 * lib.d('AlCl3', t, pa) * (pg['AlCl3'] - pe[0]) + lib.d('GaCl', t, pa) *
                              (pg['GaCl'] - pe[1]) + lib.d('HCl', t, pa) * (pg['HCl'] - pe[3]),
        lambda pe, t, pa, pg: lib.d('AlCl3', t, pa) * (pg['AlCl3'] - pe[0]) + lib.d('GaCl', t, pa) *
                              (pg['GaCl'] - pe[1]) - lib.d('NH3', t, pa) * (pg['NH3'] - pe[2]),
        lambda pe, t, pa, pg: lib.d('AlCl3', t, pa) * (pg['AlCl3'] - pe[0]) * (1 - pe[5]) - lib.d('GaCl', t, pa) * (pg['GaCl'] - pe[1]) * pe[5]
    ]

    f_prime = [
        [
            lambda pe, t, pa, pg: pe[2],
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: pe[0],
            lambda pe, t, pa, pg: -3 * k9(t, pa) * (pe[3] ** 2) * pe[5],
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: -k9(t, pa) * (pe[3] ** 3)
        ],
        [
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: pe[2],
            lambda pe, t, pa, pg: pe[1],
            lambda pe, t, pa, pg: -k10(t, pa) * (1 - pe[5]) * pe[4],
            lambda pe, t, pa, pg: -k10(t, pa) * (1 - pe[5]) * pe[3],
            lambda pe, t, pa, pg: k10(t, pa) * pe[3] * pe[4]
        ],
        [
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: -3 * lib.d('NH3', t, pa),
            lambda pe, t, pa, pg: -lib.d('HCl', t, pa),
            lambda pe, t, pa, pg: -2 * lib.d('H2', t, pa),
            lambda pe, t, pa, pg: 0
        ],
        [
            lambda pe, t, pa, pg: -3 * lib.d('AlCl3', t, pa),
            lambda pe, t, pa, pg: -lib.d('GaCl', t, pa),
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: -lib.d('HCl', t, pa),
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: 0
        ],
        [
            lambda pe, t, pa, pg: -lib.d('AlCl3', t, pa),
            lambda pe, t, pa, pg: -lib.d('GaCl', t, pa),
            lambda pe, t, pa, pg: lib.d('NH3', t, pa),
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: 0
        ],
        [
            lambda pe, t, pa, pg: -lib.d('AlCl3', t, pa) * (1 - pe[5]),
            lambda pe, t, pa, pg: lib.d('GaCl', t, pa) * pe[5],
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: 0,
            lambda pe, t, pa, pg: -lib.d('AlCl3', t, pa) * (pg['AlCl3'] - pe[0]) - lib.d('GaCl', t, pa) *
                              (pg['GaCl'] - pe[1])
        ]
    ]

    pa1 = 100000
    t = 1373
    pg1 = {
        'NH3': 1500,
        'HCl': 0
    }
    eps = 0.00001
    x = numpy.linspace(0, 1, 10)

    answers = []
    for i in x:
        answers.append(run(1, i, pa1, pg1, eps))

    v_e_AlGaN = []
    g_GaCl = []
    g_AlCl3 = []
    xp = []
    for (g, v, x_) in answers:
        v_e_AlGaN.append(v)
        g_GaCl.append(g['GaCl'])
        g_AlCl3.append(g['AlCl3'])
        xp.append(x_)

    xp1 = xp
    plt.plot(x, xp, color='blue')
    plt.ylabel('Доля $AlN$ в твердом растворе')
    plt.xlabel('Доля $AlCl_3$ в газообразных хлоридах')
    plt.grid(True)
    plt.show()

    plt.plot(x, g_GaCl, color='blue')
    plt.plot(x, g_AlCl3, color='green')
    plt.legend((r'$G_{GaCl}$', '$G_{AlCl_3}$'))
    plt.xlabel('Доля $AlCl_3$ в газообразных хлоридах')
    plt.ylabel('$G_i, кмоль/(м^{2}*с)$')
    plt.grid(True)
    plt.show()

    plt.plot(x, v_e_AlGaN, color='blue')
    plt.xlabel('Доля $AlCl_3$ в газообразных хлоридах')
    plt.ylabel('$v_{AlGaN}, нм/с$')
    plt.grid(True)
    plt.show()

    x1 = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

    answers = []
    for i in x:
        answers.append(run(2, i, pa1, pg1, eps))

    v_e_AlGaN = []
    g_GaCl = []
    g_AlCl3 = []
    xp = []
    for (g, v, x_) in answers:
        v_e_AlGaN.append(v)
        g_GaCl.append(g['GaCl'])
        g_AlCl3.append(g['AlCl3'])
        xp.append(x_)

    xp2 = xp

    plt.plot(x, xp, color='blue')
    plt.ylabel('Доля $AlN$ в твердом растворе')
    plt.xlabel('Доля $AlCl_3$ в газообразных хлоридах')
    plt.grid(True)
    plt.show()

    plt.plot(x, g_GaCl, color='blue')
    plt.plot(x, g_AlCl3, color='green')
    plt.legend((r'$G_{GaCl3}$', '$G_{AlCl}$'))
    plt.xlabel('Доля $AlCl_3$ в газообразных хлоридах')
    plt.ylabel('$G_i, кмоль/(м^{2}*с)$')
    plt.grid(True)
    plt.show()

    plt.plot(x, v_e_AlGaN, color='blue')
    plt.xlabel('Доля $AlCl_3$ в газообразных хлоридах')
    plt.ylabel('$v_{AlGaN}, нм/с$')
    plt.grid(True)
    plt.show()

    plt.plot(x, xp1)
    plt.plot(x, xp2)
    plt.ylabel('$x$', rotation=0)
    plt.xlabel('$x_{g}$')
    plt.legend(('$P^{g}_{H_{2}}/P^{g}_{N_{2}}=0$', '$P^{g}_{H_{2}}/P^{g}_{N_{2}}=1/9$'))
    plt.grid(True)
    plt.show()