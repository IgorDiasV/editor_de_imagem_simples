import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np


class EditImage():
    def __init__(self):
        self.imagem = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.is_selecting = False
        self.regiao_selecionada =False
       
    def abrir_imagem(self):
  

        self.file_path = filedialog.askopenfilename()
        self.imagem = cv2.imread(self.file_path)
        imagem_rgb = cv2.cvtColor(self.imagem, cv2.COLOR_BGR2RGB)
        imagem_tk = ImageTk.PhotoImage(Image.fromarray(imagem_rgb))

        label_imagem.configure(image=imagem_tk)
        label_imagem.image = imagem_tk


    def aplicar_filtro(self, filtro):
        


        mask = np.array(filtro).reshape(3, 3)

        if self.regiao_selecionada:
            regiao_selecionada = np.zeros_like(self.imagem[:, :, 0])
            regiao_selecionada[self.start_y:self.end_y , self.start_x: self.end_x] = 255
            imagem_aux =  self.imagem[self.start_y:self.end_y, self.start_x:self.end_x]
            frameFiltered = cv2.filter2D(imagem_aux, -1, mask, anchor=(1, 1), delta=0, borderType=cv2.BORDER_DEFAULT)
            imagem_aux = self.imagem.copy()
            for x in range(self.start_x, self.end_x):
                for y in range(self.start_y, self.end_y):
                    imagem_aux[y][x] = frameFiltered[y-self.start_y][x-self.start_x]
            frameFiltered = imagem_aux.copy()
            self.regiao_selecionada = False
       
        else:
            frameFiltered = cv2.filter2D(self.imagem.copy(), -1, mask, anchor=(1, 1), delta=0, borderType=cv2.BORDER_DEFAULT)
        # frameFiltered = cv2.convertScaleAbs(frameFiltered)

        result = np.uint8(frameFiltered)
        # cv2.imshow('blabla', result)
        # cv2.waitKey()
        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        imagem_tk = ImageTk.PhotoImage(Image.fromarray(result))
        
        label_imagem.configure(image=imagem_tk)
        
        label_imagem.image = imagem_tk
    
    def media(self):
        media = [0.1111, 0.1111, 0.1111, 0.1111, 0.1111, 0.1111, 0.1111, 0.1111, 0.1111]
        self.aplicar_filtro(media)
    def gauss(self):
        gauss = [0.0625, 0.125, 0.0625, 0.125, 0.25, 0.125, 0.0625, 0.125, 0.0625]
        self.aplicar_filtro(gauss)
    def horizontal(self):
        horizontal = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
        self.aplicar_filtro(horizontal)
    def vertical(self):
        vertical = [-1, -2, -1, 0, 0, 0, 1, 2, 1]
        self.aplicar_filtro(vertical)
    def laplacian(self):
        laplacian = [0, -1, 0, -1, 4, -1, 0, -1, 0]
        self.aplicar_filtro(laplacian)
    def boost(self):
        boost = [0, -1, 0, -1, 5.2, -1, 0, -1, 0]
        self.aplicar_filtro(boost)    
   
    def on_mouse_move(self, event):
        if self.file_path and self.is_selecting and event.widget == label_imagem:
            
            self.end_x = event.x
            self.end_y = event.y
            imagem_com_retangulo = self.imagem.copy()
            cv2.rectangle(imagem_com_retangulo, (self.start_x, self.start_y), (self.end_x, self.end_y), (255, 0, 0), 2)
            imagem_com_retangulo_rgb = cv2.cvtColor(imagem_com_retangulo, cv2.COLOR_BGR2RGB)
            imagem_tk = ImageTk.PhotoImage(Image.fromarray(imagem_com_retangulo_rgb))
            label_imagem.configure(image=imagem_tk)
            label_imagem.image = imagem_tk
   
    def on_mouse_down(self, event):
        if self.file_path and event.widget == label_imagem:
            self.start_x = event.x
            self.start_y = event.y
            self.is_selecting = True
    def on_mouse_up(self, event):
        if self.file_path and self.is_selecting:
            self.is_selecting = False
            # imagem = cv2.imread(self.file_path)
            imagem_com_retangulo = self.imagem.copy()
            cv2.rectangle(imagem_com_retangulo, (self.start_x, self.start_y), (self.end_x, self.end_y), (255, 0, 0), 2)
            imagem_com_retangulo_rgb = cv2.cvtColor(imagem_com_retangulo, cv2.COLOR_BGR2RGB)
            imagem_tk = ImageTk.PhotoImage(Image.fromarray(imagem_com_retangulo_rgb))
            label_imagem.configure(image=imagem_tk)
            label_imagem.image = imagem_tk
            self.regiao_selecionada = True 

    def iniciar_selecao(self):
        janela.bind("<Button-1>", self.on_mouse_down)
        janela.bind("<B1-Motion>", self.on_mouse_move)
        janela.bind("<ButtonRelease-1>", self.on_mouse_up)


janela = tk.Tk()
screen_width = janela.winfo_screenwidth()
screen_height = janela.winfo_screenheight()
janela.geometry(f"{screen_width}x{screen_height}")
frame_botoes = tk.Frame(janela)
frame_botoes.pack()
edit_image = EditImage()
botao_abrir_imagem = tk.Button(frame_botoes, text="Abrir Imagem", command=edit_image.abrir_imagem)
botao_media = tk.Button(frame_botoes, text="Filtro Média", command=edit_image.media)
botao_gaus = tk.Button(frame_botoes, text="Filtro Gauss", command=edit_image.gauss)
botao_horizontal = tk.Button(frame_botoes, text="Filtro Horizontal", command=edit_image.horizontal)
botao_vertical = tk.Button(frame_botoes, text="Filtro Vertical", command=edit_image.vertical)
botao_laplaciano = tk.Button(frame_botoes, text="Filtro Laplaciano", command=edit_image.laplacian)
botao_boost = tk.Button(frame_botoes, text="Filtro Boost", command=edit_image.boost)
botao_selecao = tk.Button(frame_botoes, text="Selecionar Região", command=edit_image.iniciar_selecao)

botao_abrir_imagem.grid(row=0, column=0)
botao_media.grid(row=0, column=1)
botao_gaus.grid(row=0, column=2)
botao_horizontal.grid(row=0, column=3)
botao_vertical.grid(row=0, column=4)
botao_laplaciano.grid(row=0, column=5)
botao_boost.grid(row=0, column=6)
botao_selecao.grid(row=0, column=7)

frame_imagem = tk.Frame(janela)
frame_imagem.pack()
label_imagem = tk.Label(frame_imagem)
label_imagem.pack()

janela.mainloop()
