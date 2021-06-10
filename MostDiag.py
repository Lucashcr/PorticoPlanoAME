#############################################
# EXIBIÇÃO DOS DIAGRAMAS E REAÇÕES DE APOIO #
#############################################

import tkinter
import numpy

# INICIALIZAÇÃO DA JANELA
wnview = tkinter.Tk()
wnview.title('Visualização dos Diagramas')
wnview.resizable(width=False, height=False)
frame = tkinter.Frame(wnview)
width = 800
height = 600
lim_x = int(max(X) * 100) + 200
lim_y = int(max(Y) * 100) + 200
estrut = tkinter.Canvas(frame, height=height, width=width, scrollregion=(0, 0, lim_x, lim_y))
# --------------------------------------------------------------------------------------------------------------
# DESENHO DA ESTRUTURA

apoio1g_x = tkinter.PhotoImage(file='img/Apoio1g_x.png')
apoio1g_y = tkinter.PhotoImage(file='img/Apoio1g_y.png')
apoio2g = tkinter.PhotoImage(file='img/Apoio2g.png')
apoio3g = tkinter.PhotoImage(file='img/Apoio3g.png')

def DrawEstrut(test):
    estrut.delete(tkinter.ALL)

    for i in range(0, nElem):
        xs = int(X[j[i]]) * 100 + 100
        ys = int(Y[j[i]]) * 100 + 100
        xe = int(X[k[i]]) * 100 + 100
        ye = int(Y[k[i]]) * 100 + 100
        estrut.create_line(xs, ys, xe, ye, width=2)

    for i in range(0, nNos):
        xc = int(X[i]) * 100 + 100
        yc = int(Y[i]) * 100 + 100
        x0 = xc - 5
        y0 = yc - 5
        x1 = xc + 5
        y1 = yc + 5

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

    if test:
        estrut.scale('all', 0, 0, 1, -1)
        fWidth = int(max(X, key=float)) * 100 + 250
        fHeight = int(max(Y, key=float)) * 100 + 250
        estrut.move('all', 0, fHeight)
        sc = min(width / fWidth, height / fHeight)
        estrut.scale('all', 0, 0, sc, sc)
        estrut.pack(side='right')

diag = ''
# --------------------------------------------------------------------------------------------------------------
# Esforço Normal
def DrawEsfNormal():
    global diag
    diag = 'N'
    DrawEstrut(False)
    for i in range(0, nElem):
        ang = numpy.arcsin(sn[i]) + numpy.pi / 2
        xi = X[j[i]] * 100 + 100
        yi = Y[j[i]] * 100 + 100
        x1 = xi + (Nj[i]) * numpy.cos(ang) * s.get()
        y1 = yi + (Nj[i]) * numpy.sin(ang) * s.get()
        xf = X[k[i]] * 100 + 100
        yf = Y[k[i]] * 100 + 100
        x2 = xf + (Nk[i]) * numpy.cos(ang) * s.get()
        y2 = yf + (Nk[i]) * numpy.sin(ang) * s.get()

        estrut.create_line(xi, yi, x1, y1, x2, y2, xf, yf, fill='blue', width=2)
        if Nj[i] != 0:
            estrut.create_text(x1 - 30 * (numpy.cos(ang)), y1 + 30 * (numpy.sin(ang)),
                               text=Nj[i], fill='blue', font=('Arial', 10, 'bold'))
        if Nk[i] != 0:
            estrut.create_text(x2 - 30 * (numpy.cos(ang)), y2 + 30 * (numpy.sin(ang)),
                               text=Nk[i], fill='blue', font=('Arial', 10, 'bold'))

    estrut.scale('all', 0, 0, 1, -1)
    fWidth = int(max(X, key=float)) * 100 + 250
    fHeight = int(max(Y, key=float)) * 100 + 250
    estrut.move('all', 0, fHeight)
    sc = min(width / fWidth, height / fHeight)
    estrut.scale('all', 0, 0, sc, sc)
    estrut.update()


# --------------------------------------------------------------------------------------------------------------
# Esforço Cortante
def DrawEsfCortante():
    global diag
    diag = 'Q'
    DrawEstrut(False)
    for i in range(0, nElem):
        ang = numpy.arcsin(sn[i]) + numpy.pi / 2
        xi = X[j[i]] * 100 + 100
        yi = Y[j[i]] * 100 + 100
        x1 = xi + (Qj[i]) * numpy.cos(ang) * s.get()
        y1 = yi + (Qj[i]) * numpy.sin(ang) * s.get()
        xf = X[k[i]] * 100 + 100
        yf = Y[k[i]] * 100 + 100
        x2 = xf + (Qk[i]) * numpy.cos(ang) * s.get()
        y2 = yf + (Qk[i]) * numpy.sin(ang) * s.get()

        estrut.create_line(xi, yi, x1, y1, x2, y2, xf, yf, fill='green', width=2)
        if Qj[i] != 0:
            estrut.create_text(x1 - 30 * (numpy.cos(ang)), y1 + 30 * (numpy.sin(ang)),
                               text=Qj[i], fill='green', font=('Arial', 10, 'bold'))
        if Qk[i] != 0:
            estrut.create_text(x2 - 30 * (numpy.cos(ang)), y2 + 30 * (numpy.sin(ang)),
                               text=Qk[i], fill='green', font=('Arial', 10, 'bold'))

    estrut.scale('all', 0, 0, 1, -1)
    fWidth = int(max(X, key=float)) * 100 + 250
    fHeight = int(max(Y, key=float)) * 100 + 250
    estrut.move('all', 0, fHeight)
    sc = min(width / fWidth, height / fHeight)
    estrut.scale('all', 0, 0, sc, sc)
    estrut.update()


# --------------------------------------------------------------------------------------------------------------
# Momento Fletor
def DrawMomFletor():
    global diag
    diag = 'M'
    DrawEstrut(False)
    for i in range(0, nElem):
        ang = numpy.arcsin(sn[i]) + numpy.pi / 2
        xi = X[j[i]] * 100 + 100
        yi = Y[j[i]] * 100 + 100
        x1 = xi - (Mj[i]) * numpy.cos(ang) * s.get()
        y1 = yi - (Mj[i]) * numpy.sin(ang) * s.get()
        xf = X[k[i]] * 100 + 100
        yf = Y[k[i]] * 100 + 100
        x2 = xf - (Mk[i]) * numpy.cos(ang) * s.get()
        y2 = yf - (Mk[i]) * numpy.sin(ang) * s.get()

        estrut.create_line(xi, yi, x1, y1, fill='orange', width=2)
        if Mj[i] != 0:
            estrut.create_text(x1 - 30 * abs(numpy.cos(ang)), y1 + 30 * abs(numpy.sin(ang)),
                               text=Mj[i], fill='orange', font=('Arial', 10, 'bold'))

        if qx[i] != 0 or qy[i] != 0:
            xm = (xi + xf) / 2 - (qx[i] * L[i] ** 2 / 8) * numpy.cos(ang) * s.get()
            ym = (yi + yf) / 2 - (qy[i] * L[i] ** 2 / 8) * numpy.sin(ang) * s.get()

            estrut.create_line(x1, y1, xm, ym, x2, y2, fill='orange', smooth=1, width=2)
        else:
            estrut.create_line(x1, y1, x2, y2, fill='orange', width=2)

        estrut.create_line(x2, y2, xf, yf, fill='orange', width=2)
        if Mk[i] != 0:
            estrut.create_text(x2 - 30 * abs(numpy.cos(ang)), y2 - 30 * abs(numpy.sin(ang)),
                               text=Mk[i], fill='orange', font=('Arial', 10, 'bold'))

    estrut.scale('all', 0, 0, 1, -1)
    fWidth = int(max(X, key=float)) * 100 + 250
    fHeight = int(max(Y, key=float)) * 100 + 250
    estrut.move('all', 0, fHeight)
    sc = min(width / fWidth, height / fHeight)
    estrut.scale('all', 0, 0, sc, sc)
    estrut.update()

#-----------------------------------------------------------------------------------------------------------------------
# Reações de apoio

def DrawRap():
    global diag
    diag = ''
    DrawEstrut(False)
    for n in range(0, nNos):
        CreateSeta('x', n, Rx[n])
        CreateSeta('y', n, Ry[n])
        CreateSeta('z', n, Rz[n])

    estrut.scale('all', 0, 0, 1, -1)
    fWidth = int(max(X, key=float)) * 100 + 250
    fHeight = int(max(Y, key=float)) * 100 + 250
    estrut.move('all', 0, fHeight)
    sc = min(width / fWidth, height / fHeight)
    estrut.scale('all', 0, 0, sc, sc)
    estrut.update()
#-----------------------------------------------------------------------------------------------------------------------
# Escalonamento dos diagramas na janela com slider
def escalDiag(v):
    if diag == 'N':
        DrawEsfNormal()
    elif diag == 'Q':
        DrawEsfCortante()
    elif diag == 'M':
        DrawMomFletor()

s = tkinter.Scale(wnview, from_=20, to=0, resolution=0.1, orient='vertical',
                  length=500, label='Escala', command=escalDiag)
s.pack(side=tkinter.RIGHT)
s.set(1)
frame.pack()

# Definição dos botões
b_EsfN = tkinter.Button(wnview, text="Esforço Normal", command=DrawEsfNormal, width=30)
b_EsfN.pack(side=tkinter.LEFT)
b_EsfC = tkinter.Button(wnview, text="Esforço Cortante", command=DrawEsfCortante, width=30)
b_EsfC.pack(side=tkinter.LEFT)
b_MomF = tkinter.Button(wnview, text="Momento Fletor", command=DrawMomFletor, width=30)
b_MomF.pack(side=tkinter.LEFT)
b_Rap = tkinter.Button(wnview, text="Reações de Apoio", command=DrawRap, width=30)
b_Rap.pack(side=tkinter.LEFT)

DrawEstrut(True)

wnview.eval('tk::PlaceWindow . center')
wnview.mainloop()
