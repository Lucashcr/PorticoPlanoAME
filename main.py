#######################################################
# MÓDULO: EXECUTA CADA PACOTE NA SUA RESPECTIVA ORDEM #
#######################################################

# Lembrando que, para que o programa funcione corretamente
# todos os módulos precisam estar no mesmo diretório

import tkinter
from tkinter import messagebox
from tkinter import ttk
import os

if __name__ == '__main__':
    # Criação do elemento de janela
    window = tkinter.Tk()
    window.title('Pórtico Plano AME')

    # Definição dos botões de seleção "Sim" e "Não"
    gd = tkinter.StringVar(window, '1')
    tkinter.Checkbutton(window, text = "Gerar diagramas", variable = gd,
            onvalue = 1, offvalue = 0).pack(side = tkinter.TOP, ipady = 5)
            
    # Varredura na pasta \ent buscando arquivos Excel de entrada de dados
    pasta = '.\ent'
    arq = list()
    for diretorio, subpastas, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            if arquivo[-4:] == 'xlsx' or '.xls':
                arq.append(os.path.join(diretorio, arquivo))

    # Criação do ComboBox com os arquivos Excel de entrada de dados para escolha 
    combobox = ttk.Combobox(window, textvariable=arq, width=50, values = arq)
    combobox.pack()

    # Função de chamada do botão "Executar" - 
    # Passa o diretório do arquivo escolhido para fPath 
    # e fecha a jaenla, continuando o programa
    def cont_prog():
        global fPath
        fPath = combobox.get() + ' '
        global op
        op = gd.get()
        window.destroy()
        
    # Definição do objeto botão "Executar"
    button_run = tkinter.Button(window,
                            text = 'Executar',
                            command = cont_prog,
                            width = 15)
    button_run.pack(side=tkinter.LEFT)
   
    # Definição do objeto botão "Fechar"
    button_exit = tkinter.Button(window,
                         text = 'Fechar',
                         command = quit,
                         width = 15)
    button_exit.pack(side=tkinter.RIGHT)
  
    #Loop de eventos da janela
    window.mainloop()

    # Confere a entrada do arquivo e chama a execução dos demais módulos
    
    try:
        exec(open('EntDados.py').read())
        exec(open('ConfirmEstrut.py').read())
        exec(open('AnMatric.py').read())
        exec(open('Resultados.py').read())
        if op == '1':
            exec(open('MostDiag.py').read())

            #Aguarda o encerramento do programa
        input('\nPressione Enter para finalizar...')
    except:
        tkinter.messagebox.showerror(title='Erro...', message='Erro na especificação ou nos dados do arquivo!')