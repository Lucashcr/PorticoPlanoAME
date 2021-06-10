#############################################################################
# MÓDULO: OBTENÇÃO DOS ESFORÇOS INTERNOS, REAÇÕES DE APOIO E DESLOCAMENTOS #
#############################################################################

import numpy
import pandas

Nj = numpy.zeros(nElem)
Qj = numpy.zeros(nElem)
Mj = numpy.zeros(nElem)
Nk = numpy.zeros(nElem)
Qk = numpy.zeros(nElem)
Mk = numpy.zeros(nElem)
Rap = numpy.zeros(3 * nNos)
Rx = numpy.zeros(nNos)
Ry = numpy.zeros(nNos)
Rz = numpy.zeros(nNos)
dx = numpy.zeros(nNos)
dy = numpy.zeros(nNos)
dz = numpy.zeros(nNos)

for i in range(0, nElem):
    # Definindo matriz de rigidez local do elemento
    A = EA[i] / L[i]
    B = 12 * EI[i] / L[i] ** 3
    C = 6 * EI[i] / L[i] ** 2
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

    # Obtendo o vetores de deslocamentos e ações locais do elemento
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

    v_pos = [
        3 * j[i],
        3 * j[i] + 1,
        3 * j[i] + 2,
        3 * k[i],
        3 * k[i] + 1,
        3 * k[i] + 2
    ]
    D_g = numpy.zeros(6)
    for lin in range(0, 6):
        D_g[lin] = d[v_pos[lin]]
    D_e = beta_e.dot(D_g)
    P_e = Pne_e + r_e.dot(D_e)

    # Definindo os vetores de esforços internos solicitantes
    Nj[i] = numpy.around(P_e[0], decimals=4)
    Qj[i] = numpy.around(P_e[1], decimals=4)
    Mj[i] = numpy.around(P_e[2], decimals=4)
    Nk[i] = numpy.around(P_e[3], decimals=4)
    Qk[i] = numpy.around(P_e[4], decimals=4)
    Mk[i] = numpy.around(P_e[5], decimals=4)

    # Definindo vetor de reações de apoio geral
    P_g = beta_e.transpose().dot(P_e)
    for lin in range(0, 6):
        Rap[v_pos[lin]] += P_g[lin]

for c in range(0, nNos):
    # Separando vetor de reações de apoio geral pelo eixo
    Rx[c] = numpy.around(Rap[3 * c] - Fn[3 * c], decimals=4)
    Ry[c] = numpy.around(Rap[3 * c + 1] - Fn[3 * c + 1], decimals=4)
    Rz[c] = numpy.around(Rap[3 * c + 2] - Fn[3 * c + 2], decimals=4)

    # Separando vetor de deslocamentos geral pelo eixo
    dx[c] = numpy.around(d[3 * c], decimals=6)
    dy[c] = numpy.around(d[3 * c + 1], decimals=6)
    dz[c] = numpy.around(d[3 * c + 2], decimals=6)

# Saída dos dados no terminal
N_Result = pandas.DataFrame({'Barra': range(1, nElem+1), 'Nó j': j+1, 'Nó k': k+1,
                             'Esforço Normal j': Nj, 'Esforço Normal k': Nk})
print(N_Result.to_string(index=False), '\n')

Q_Result = pandas.DataFrame({'Barra': range(1, nElem+1), 'Nó j': j+1, 'Nó k': k+1,
                             'Esforço Cortante j': Qj, 'Esforço Cortante k': Qk})
print(Q_Result.to_string(index=False), '\n')

M_Result = pandas.DataFrame({'Barra': range(1, nElem+1), 'Nó j': j+1, 'Nó k': k+1,
                             'Momento Fletor j': Mj, 'Momento Fletor k': Mk})
print(M_Result.to_string(index=False), '\n')

Rap_result = pandas.DataFrame({'Nó': range(1, nNos+1), 'Reação Horizontal': Rx,
                               'Reação vertical': Ry, 'Reação Momento': Rz})
print(Rap_result.to_string(index=False), '\n')

d_result = pandas.DataFrame({'Nó': range(1, nNos+1), 'Desloc Horizontal': dx,
                               'Desloc vertical': dy, 'Rotação': dz})
print(d_result.to_string(index=False))

# Saída dos dados em um arquivo txt de mesmo nome
# do arquivo de entrada
fOut = fPath.replace('ent', 'out')
if fPath[-5:] == 'xlsx ':
    fOut = fOut.replace('xlsx', 'txt')
else: 
    fOut = fOut.replace('xls', 'txt')

with open(fOut, 'w') as arqout:
    arqout.writelines(N_Result.to_string(index=False) + '\n\n')
    arqout.writelines(Q_Result.to_string(index=False) + '\n\n')
    arqout.writelines(M_Result.to_string(index=False) + '\n\n')
    arqout.writelines(Rap_result.to_string(index=False) + '\n\n')
    arqout.writelines(d_result.to_string(index=False) + '\n\n')
    
print('\nDados armazenados no arquivo: ', fOut)