########################################################
# MÓDULO: REALIZAÇÃO DOS CÁLCULOS DE ANÁLISE MATRICIAL #
########################################################
import math
import numpy

# OBTENÇÃO DA MATRIZ [R]
R = numpy.zeros((3 * nNos, 3 * nNos))
for i in range(0, nElem):
    # Definindo matriz de rigidez local do elemento
    A = EA[i] / L[i]
    B = 12 * EI[i] / (L[i] ** 3)
    C = 6 * EI[i] / (L[i] ** 2)
    D = 2 * EI[i] / L[i]
    r_e = numpy.array([
        [A, 0, 0, A, 0, 0],
        [0, B, -C, 0, B, C],
        [0, -C, 2 * D, 0, -C, -D],
        [A, 0, 0, A, 0, 0],
        [0, B, -C, 0, B, C],
        [0, C, -D, 0, C, 2 * D]
    ], dtype=float)

    # Definindo matriz de incidência cinemática do elemento
    beta_e = numpy.array([
        [-cs[i], -sn[i], 0, 0, 0, 0],
        [-sn[i], cs[i], 0, 0, 0, 0],
        [0, 0, -1, 0, 0, 0],
        [0, 0, 0, cs[i], sn[i], 0],
        [0, 0, 0, sn[i], -cs[i], 0],
        [0, 0, 0, 0, 0, 1]
    ], dtype=float)

    # Definindo matriz de rigidez global do elemento pelo triplo produto matricial
    r_g = numpy.linalg.multi_dot([beta_e.transpose(), r_e, beta_e])

    # Locando os elementos da matriz de rigidez global do elemento em sua respectiva posição de R
    v_pos = [
        3 * j[i],
        3 * j[i] + 1,
        3 * j[i] + 2,
        3 * k[i],
        3 * k[i] + 1,
        3 * k[i] + 2
    ]
    for lin in range(0, 6):
        for col in range(0, 6):
            R[v_pos[lin], v_pos[col]] += r_g[lin, col]

# -----------------------------------------------------------------------------------------------------------------------
# OBTENÇÃO DO VETOR DE AÇÕES GLOBAIS

# DETERMINAÇÃO DO VETOR DE AÇÕES NODAIS EQUIVALENTES
Fne = numpy.zeros(3 * nNos)
for i in range(0, nElem):
    # Definindo matriz de incidência cinemática do elemento
    beta_e = numpy.array([
        [-cs[i], -sn[i], 0, 0, 0, 0],
        [-sn[i], cs[i], 0, 0, 0, 0],
        [0, 0, -1, 0, 0, 0],
        [0, 0, 0, cs[i], sn[i], 0],
        [0, 0, 0, sn[i], -cs[i], 0],
        [0, 0, 0, 0, 0, 1]
    ], dtype=float)

    # Definindo vetor de ações nodais local equivalentes
    qxe = qx[i] * cs[i] - qy[i] * sn[i]
    qye = qx[i] * sn[i] + qy[i] * cs[i]
    Pne_e = numpy.array([
        qxe * L[i] / 2,
        qye * L[i] / 2,
        - qye * L[i] ** 2 / 12,
        - qxe * L[i] / 2,
        - qye * L[i] / 2,
        - qye * L[i] ** 2 / 12
    ])

    # Transformando vetor de ações local para global
    Pne_g = beta_e.transpose().dot(Pne_e)

    # Locando os elementos da vetor de ações global do elemento em sua respectiva posição
    # do vetor de ações global da estrutura
    v_pos = [
        3 * j[i],
        3 * j[i] + 1,
        3 * j[i] + 2,
        3 * k[i],
        3 * k[i] + 1,
        3 * k[i] + 2
    ]
    for lin in range(0, len(v_pos)):
        Fne[v_pos[lin]] -= Pne_g[lin]

# Obtenção do vetor de ações global pelo somatório das ações nodais reais e equivalentes
F = Fne + Fn
# ----------------------------------------------------------------------------------------------------------------------
# CÁLCULO DOS DESLOCAMENTOS GLOBAIS

# Técnica do penalty para aplicar as condições de contorno
for i in range(0, 3 * nNos):
    if Cod[i]:
        R[i, i] *= 1000000000
        F[i] = Fn[i] * 1000000000
        #R[i, :] = 0
        #R[:, i] = 0
        #R[i, i] = 1
        #F[i] = 0

# Resoluçao do sistema
d = numpy.linalg.solve(R, F)
