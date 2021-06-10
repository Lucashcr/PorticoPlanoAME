###########################################################################
# MÓDULO: VIZUALIZAÇÃO DA ESTRUTURA PARA CONFERÊNCIA DA ENTRADA DOS DADOS #
###########################################################################
import tkinter
import tkinter.messagebox
import numpy

# Inicialização da janela
wnview = tkinter.Tk()
wnview.title('Visualização da Estrutura')
wnview.resizable(width=False, height=False)
frame = tkinter.Frame(wnview)
frame.pack()
width = 800
height = 600
lim_x = int(max(X) * 100) + 200
lim_y = int(max(Y) * 100) + 200
estrut = tkinter.Canvas(frame, height=height, width=width, scrollregion=(0, 0, lim_x, lim_y))
# ----------------------------------------------------------------------------------------------------------------------
# DESENHO DA ESTRUTURA

# Desenho das barras
for i in range(0, nElem):
    xs = int(X[j[i]]) * 100 + 100
    ys = int(Y[j[i]]) * 100 + 100
    xe = int(X[k[i]]) * 100 + 100
    ye = int(Y[k[i]]) * 100 + 100
    estrut.create_line(xs, ys, xe, ye, width=2)

# Desenho dos apoios
apoio1g_x = tkinter.PhotoImage(file='img/Apoio1g_x.png')
apoio1g_y = tkinter.PhotoImage(file='img/Apoio1g_y.png')
apoio2g = tkinter.PhotoImage(file='img/Apoio2g.png')
apoio3g = tkinter.PhotoImage(file='img/Apoio3g.png')

for i in range(0, nNos):
    xc = int(X[i]) * 100 + 100
    yc = int(Y[i]) * 100 + 100
    x0 = xc - 5
    y0 = yc - 5
    x1 = xc + 5
    y1 = yc + 5

    estrut.create_text(xc - 20, yc + 20, font=(12), text=i + 1)

    if UX[i] == 1 and UY[i] == 1 and UZ[i] == 1:
        estrut.create_image(xc, yc, image=apoio3g)

    if UX[i] == 1 and UY[i] == 1 and UZ[i] == 0:
        estrut.create_image(xc, yc, image=apoio2g)
        estrut.create_oval(x0, y0, x1, y1, fill='white', width=2)

    if UX[i] == 1 and UY[i] == 0 and UZ[i] == 0:
        estrut.create_image(xc, yc, image=apoio1g_x)
        estrut.create_oval(x0, y0, x1, y1, fill='white', width=2)

    if UX[i] == 0 and UY[i] == 1 and UZ[i] == 0:
        estrut.create_image(xc, yc, image=apoio1g_y)
        estrut.create_oval(x0, y0, x1, y1, fill='white', width=2)


# ----------------------------------------------------------------------------------------------------------------------
# DESENHO DAS CARGAS NODAIS

# Definindo função para desenho das setas
def CreateSeta(direct, id_No, F):
    if F != 0:
        xn = X[id_No] * 100 + 100
        yn = Y[id_No] * 100 + 100

        if direct == 'x':
            x2 = xn + (F / abs(F)) * 80
            y2 = yn
            x3 = x2 - (F / abs(F)) * 10
            y3 = y2 + (F / abs(F)) * 10
            x4 = x2 - (F / abs(F)) * 10
            y4 = y2 - (F / abs(F)) * 10
            estrut.create_line(xn, yn, x2, y2, x3, y3, x2, y2, x4, y4, fill='red', width=2)
            estrut.create_text(x2 + 20, y2 + 20, text=abs(F), fill='red')

        if direct == 'y':
            x2 = xn
            y2 = yn + (F / abs(F)) * 80
            x3 = x2 - (F / abs(F)) * 10
            y3 = y2 - (F / abs(F)) * 10
            x4 = x2 + (F / abs(F)) * 10
            y4 = y2 - (F / abs(F)) * 10
            estrut.create_line(xn, yn, x2, y2, x3, y3, x2, y2, x4, y4, fill='red', width=2)
            estrut.create_text(x2 + 20, y2 + 20, text=abs(F), fill='red')

        if direct == 'z':
            x_ie = xn - 50
            y_ie = yn - 50
            x_sd = xn + 50
            y_sd = yn + 50

            xf = xn
            yf = yn + (F / abs(F)) * 50
            x3 = xf + 10
            y3 = yf - 10
            x4 = xf + 10
            y4 = yf + 10

            estrut.create_arc(x_ie, y_ie, x_sd, y_sd, start=-90, extent=180, outline='red', width=2, style=tkinter.ARC)
            estrut.create_line(xf, yf, x3, y3, xf, yf, x4, y4, fill='red', width=2)
            estrut.create_text(x_sd + 5, y_sd + 5, text=abs(F), fill='red')


# Desenho de cada força nodal (chamando função CreateSeta)
for n in range(0, nNos):
    CreateSeta('x', n, FX[n])
    CreateSeta('y', n, FY[n])
    CreateSeta('z', n, MZ[n])


# ----------------------------------------------------------------------------------------------------------------------
# PROPRIEDADES DAS BARRAS


def PropBar(elem, qxi, qyi, Li, EAi, EIi):
    ang = numpy.arcsin(sn[elem]) * 180 / numpy.pi
    xm = ((X[j[elem]] * 100 + 100) + (X[k[elem]] * 100 + 100)) / 2
    ym = ((Y[j[elem]] * 100 + 100) + (Y[k[elem]] * 100 + 100)) / 2

    if qxi != 0 and qyi != 0:
        estrut.create_text(xm - abs(sn[elem]) * 25, ym + abs(float(cs[elem])) * 25, angle=ang,
                           text='Barra ' + str(elem + 1) + ' || qx = ' + str(qxi) + ' || qy = ' + str(qyi),
                           fill='green', font=('Arial', 10, 'bold'))

    if qxi != 0 and qyi == 0:
        estrut.create_text(xm - abs(sn[elem]) * 25, ym + abs(float(cs[elem])) * 25, angle=ang,
                           text='Barra ' + str(elem + 1) + ' || qx = ' + str(qxi), fill='green', font=('Arial', 10, 'bold'))

    if qxi == 0 and qyi != 0:
        estrut.create_text(xm - abs(sn[elem]) * 25, ym + abs(float(cs[elem])) * 25, angle=ang,
                           text='Barra ' + str(elem + 1) + ' || qy = ' + str(qyi), fill='green', font=('Arial', 10, 'bold'))

    if qxi == 0 and qyi == 0:
        estrut.create_text(xm - abs(sn[elem]) * 25, ym + abs(cs[elem]) * 25, angle=ang,
                           text='Barra ' + str(elem + 1), fill='green', font=('Arial', 10, 'bold'))

    estrut.create_text(xm + abs(sn[elem]) * 25, ym - abs(float(cs[elem])) * 25,
                       angle=ang, text='L = ' + str(Li) + ' || EA = ' + str(EAi) + ' || EI = ' + str(EIi), fill='green', font=('Arial', 10, 'bold'))


# Identificando propriedades das barras (chamando a função Propbar)
for i in range(0, nElem):
    PropBar(i, float(qx[i]), float(qy[i]), numpy.around(L[i], decimals=2), float(EA[i]), float(EI[i]))

# ----------------------------------------------------------------------------------------------------------------------
# AJUSTANDO IMAGEM À TELA
estrut.scale('all', 0, 0, 1, -1)
fWidth = int(max(X, key=float)) * 100 + 250
fHeight = int(max(Y, key=float)) * 100 + 250
estrut.move('all', 0, fHeight)
sc = min(width / fWidth, height / fHeight)
estrut.scale('all', 0, 0, sc, sc)
estrut.pack(fill='both')

# ----------------------------------------------------------------------------------------------------------------------
# CONSTRUÇÃO DOS BOTÕES E RESPECTIVOS MÉTODOS DE COMANDO
def accept():
    wnview.destroy()

def decline():
    tkinter.messagebox.showinfo(title='Fechando...', message='Programa interrompido pelo usuário!\n'
                                                             'Redefinir o arquivo de entrada de dados!')
    quit()

# Definição dos botões
acc = tkinter.Button(wnview, text="Continuar análise!", command=accept, width=30)
acc.pack(side=tkinter.LEFT)
dec = tkinter.Button(wnview, text="Redefinir estrutura!", command=decline, width=30)
dec.pack(side=tkinter.RIGHT)

wnview.eval('tk::PlaceWindow . center')
wnview.mainloop()
