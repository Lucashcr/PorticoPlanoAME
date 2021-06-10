###############################################
# MÓDULO: ENTRADA DE DADOS VIA PLANILHA EXCEL #
###############################################
import math
import pandas
import numpy

# Obtendo dados do arquivo de tabela e armazenando num dataframe
pQtdades = pandas.read_excel(fPath, sheet_name='Qtdades', header=0)
pDefNos = pandas.read_excel(fPath, sheet_name='DefNos', header=2)
pDefElem = pandas.read_excel(fPath, sheet_name='DefElem', header=1)

# Quantidade de nós e de elementos
nNos = pQtdades['qtdadeNos'][0]
nElem = pQtdades['qtdadeElem'][0]

# Função para definir vetores associados aos nós
def defVectorN(col, df_table, t):
    VecName = numpy.zeros(nNos, dtype=t)
    for it in range(0, nNos):
        if df_table.shape[0] != nNos or math.isnan(df_table[col][it]):
            print('Entrada dos nós incompatível...')
            quit()
        else:
            VecName[it] = numpy.array(df_table[col][it])

    return VecName

# Função para definir vetores associados aos elementos
def defVectorE(col, df_table, t):
    VecName = numpy.zeros(nElem, dtype=t)
    
    if col == 'nó j' or col == 'nó k':
        aux = 1
    else:
        aux = 0

    for it in range(0, nElem):
        if df_table.shape[0] != nElem or math.isnan(df_table[col][it]):
            print('Entrada dos elementos incompatível...')
            quit()
        else:
            VecName[it] = numpy.array(df_table[col][it] - aux)

    return VecName

# Definindo os vetores relativos aos nós (chamando função defVectorN)
X = defVectorN('x', pDefNos, float)
Y = defVectorN('y', pDefNos, float)
UX = defVectorN('ux', pDefNos, bool)
UY = defVectorN('uy', pDefNos, bool)
UZ = defVectorN('uz', pDefNos, bool)
FX = defVectorN('Fx', pDefNos, float)
FY = defVectorN('Fy', pDefNos, float)
MZ = defVectorN('Mz', pDefNos, float)

# Definindo vetor de forças globais
Fn = numpy.zeros(3 * nNos)
for i in range(0, nNos):
    Fn[3 * i] = FX[i]
    Fn[3 * i + 1] = FY[i]
    Fn[3 * i + 2] = MZ[i]

# Definindo vetor de condições de contorno
Cod = numpy.zeros(3 * nNos)
for i in range(0, nNos):
    Cod[3 * i] = UX[i]
    Cod[3 * i + 1] = UY[i]
    Cod[3 * i + 2] = UZ[i]

# Definindo os vetores relativos aos elementos (chamando função defVectorE)
j = defVectorE('nó j', pDefElem, int)
k = defVectorE('nó k', pDefElem, int)
EA = defVectorE('EA', pDefElem, float)
EI = defVectorE('EI', pDefElem, float)
qx = defVectorE('qx', pDefElem, float)
qy = defVectorE('qy', pDefElem, float)

# Calculando e definindo os vetores de comprimento, seno e cosseno dos elementos
L = numpy.zeros(nElem, dtype=float)
cs = numpy.zeros(nElem, dtype=float)
sn = numpy.zeros(nElem, dtype=float)
for i in range(0, nElem):
    L[i] = numpy.sqrt(numpy.square(X[k[i]] - X[j[i]]) + numpy.square(Y[k[i]] - Y[j[i]]))
    cs[i] = (X[k[i]] - X[j[i]]) / L[i]
    sn[i] = (Y[k[i]] - Y[j[i]]) / L[i]