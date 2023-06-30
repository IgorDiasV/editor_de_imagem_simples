import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np

imagem = ''
def abrir_imagem():
    global imagem

    file_path = filedialog.askopenfilename()
    imagem = cv2.imread(file_path)
    imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    imagem_tk = ImageTk.PhotoImage(Image.fromarray(imagem))

    label_imagem.configure(image=imagem_tk)
    label_imagem.image = imagem_tk


def aplicar_filtro(filtro):
    
    mask = np.array(filtro).reshape(3, 3)
    frameFiltered = cv2.filter2D(imagem, -1, mask, anchor=(1, 1), delta=0, borderType=cv2.BORDER_DEFAULT)
    # frameFiltered = cv2.convertScaleAbs(frameFiltered)
    result = np.uint8(frameFiltered)

    imagem_tk = ImageTk.PhotoImage(Image.fromarray(result))
    
    label_imagem.configure(image=imagem_tk)
    
    label_imagem.image = imagem_tk
    
def media():
    media = [0.1111, 0.1111, 0.1111, 0.1111, 0.1111, 0.1111, 0.1111, 0.1111, 0.1111]
    aplicar_filtro(media)
def gauss():
    gauss = [0.0625, 0.125, 0.0625, 0.125, 0.25, 0.125, 0.0625, 0.125, 0.0625]
    aplicar_filtro(gauss)
def horizontal():
    horizontal = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
    aplicar_filtro(horizontal)
def vertical():
    vertical = [-1, -2, -1, 0, 0, 0, 1, 2, 1]
    aplicar_filtro(vertical)
def laplacian():
    laplacian = [0, -1, 0, -1, 4, -1, 0, -1, 0]
    aplicar_filtro(laplacian)
def boost():
    boost = [0, -1, 0, -1, 5.2, -1, 0, -1, 0]
    aplicar_filtro(boost)    


janela = tk.Tk()
janela.geometry("600x600")

frame_botoes = tk.Frame(janela)
frame_botoes.pack()

botao_abrir_imagem = tk.Button(frame_botoes, text="Abrir Imagem", command=abrir_imagem)
botao_media = tk.Button(frame_botoes, text="Filtro Média", command=media)
botao_gaus = tk.Button(frame_botoes, text="Filtro Gauss", command=gauss)
botao_horizontal = tk.Button(frame_botoes, text="Filtro Horizontal", command=horizontal)
botao_vertical = tk.Button(frame_botoes, text="Filtro Vertical", command=vertical)
botao_laplaciano = tk.Button(frame_botoes, text="Filtro Laplaciano", command=laplacian)
botao_boost = tk.Button(frame_botoes, text="Filtro Boost", command=boost)

botao_abrir_imagem.grid(row=0, column=0)
botao_media.grid(row=0, column=1)
botao_gaus.grid(row=0, column=2)
botao_horizontal.grid(row=0, column=3)
botao_vertical.grid(row=0, column=4)
botao_laplaciano.grid(row=0, column=5)
botao_boost.grid(row=0, column=6)

frame_imagem = tk.Frame(janela)
frame_imagem.pack()
label_imagem = tk.Label(frame_imagem)
label_imagem.pack()

janela.mainloop()
