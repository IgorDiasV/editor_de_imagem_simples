import cv2
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np
from tkinter import colorchooser

class EditImage():
    def __init__(self, janela,label_imagem):
        self.imagem = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.is_selecting = False
        self.regiao_selecionada =False
        self.imagem_original = None
        # self.imagem_anterior = None
        self.label_imagem = label_imagem
        self.janela = janela
        self.hist_alteracao =  [None for i in range(5)]
        self.post_atual = 0
       
    def abrir_imagem(self):
  

        self.file_path = filedialog.askopenfilename()
        self.imagem = cv2.imread(self.file_path)
        self.imagem_original = self.imagem.copy()
        self.hist_alteracao[self.post_atual] = self.imagem.copy()
        self.post_atual += 1
        imagem_rgb = cv2.cvtColor(self.imagem, cv2.COLOR_BGR2RGB)
        imagem_tk = ImageTk.PhotoImage(Image.fromarray(imagem_rgb))
        self.label_imagem.configure(image=imagem_tk)
        self.label_imagem.image = imagem_tk


    def aplicar_filtro(self, filtro):      

        mask = np.array(filtro).reshape(3, 3)
        
        if self.post_atual == 5:
            self.hist_alteracao.pop(0)
            self.hist_alteracao.append(self.imagem.copy())
        else:
            self.hist_alteracao[self.post_atual] = self.imagem.copy()
            self.post_atual += 1

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

        result = np.uint8(frameFiltered)
        self.imagem = result.copy()
        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        imagem_tk = ImageTk.PhotoImage(Image.fromarray(result))
        
        self.label_imagem.configure(image=imagem_tk)
        
        self.label_imagem.image = imagem_tk
    
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
        if self.file_path and self.is_selecting and event.widget == self.label_imagem:
            
            self.end_x = event.x
            self.end_y = event.y
            imagem_com_retangulo = self.imagem.copy()
            cv2.rectangle(imagem_com_retangulo, (self.start_x, self.start_y), (self.end_x, self.end_y), (255, 0, 0), 2)
            
            imagem_com_retangulo_rgb = cv2.cvtColor(imagem_com_retangulo, cv2.COLOR_BGR2RGB)
            imagem_tk = ImageTk.PhotoImage(Image.fromarray(imagem_com_retangulo_rgb))
            self.label_imagem.configure(image=imagem_tk)
            self.label_imagem.image = imagem_tk
   
    def on_mouse_down(self, event):
        if self.file_path and event.widget == self.label_imagem:
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
            self.label_imagem.configure(image=imagem_tk)
            self.label_imagem.image = imagem_tk
            self.regiao_selecionada = True 

    def restaurar_imagem(self):
        self.imagem = self.imagem_original.copy()
        resultado = cv2.cvtColor(self.imagem, cv2.COLOR_BGR2RGB)
        imagem_tk = ImageTk.PhotoImage(Image.fromarray( resultado))
        self.label_imagem.configure(image=imagem_tk)
        self.label_imagem.image = imagem_tk
        
    def desfazer_alteracao(self):
        if(self.post_atual>0):
            self.post_atual -= 1
            self.imagem = self.hist_alteracao[self.post_atual].copy()
            resultado = cv2.cvtColor(self.imagem, cv2.COLOR_BGR2RGB)
            imagem_tk = ImageTk.PhotoImage(Image.fromarray( resultado))
            self.label_imagem.configure(image=imagem_tk)
            self.label_imagem.image = imagem_tk

    def iniciar_selecao(self):
        self.janela.bind("<Button-1>", self.on_mouse_down)
        self.janela.bind("<B1-Motion>", self.on_mouse_move)
        self.janela.bind("<ButtonRelease-1>", self.on_mouse_up)

    
    def regiao_clicada(self):
        self.janela.bind("<Button-1>", self.detectar_cor)
    def detectar_cor(self, event):
        if event.widget == self.label_imagem:
            pixel = self.imagem[event.y, event.x]
            self.b = pixel[0]
            self.g = pixel[1]
            self.r = pixel[2]
            print(pixel)
    
    def mudar_cor(self):
        color = colorchooser.askcolor(title="Escolha uma cor")    
        rgb = color[0]
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        altura = np.shape(self.imagem)[0]
        largura = np.shape(self.imagem)[1]
        for i in range(altura):
            for j in range(largura):
                pixel = self.imagem[i, j]
                if (pixel[0] >= (self.b - 10) and pixel[0] <= (self.b+10) )  and (pixel[1] >= (self.g - 10) and pixel[1] <= (self.g+10) ) and (pixel[2] >= (self.r - 10) and (pixel[2] <= (self.r+10)) ):
                    self.imagem[i, j] = [b, g, r]

        resultado = cv2.cvtColor(self.imagem, cv2.COLOR_BGR2RGB)
        imagem_tk = ImageTk.PhotoImage(Image.fromarray( resultado))
        self.label_imagem.configure(image=imagem_tk)
        self.label_imagem.image = imagem_tk