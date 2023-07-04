import tkinter as tk
from editor_imagem import EditImage



janela = tk.Tk()
screen_width = janela.winfo_screenwidth()
screen_height = janela.winfo_screenheight()
janela.geometry(f"{screen_width}x{screen_height}")
frame_botoes = tk.Frame(janela)
frame_botoes.pack()
frame_imagem = tk.Frame(janela)
label_imagem = tk.Label(frame_imagem)

edit_image = EditImage(janela, label_imagem)
botao_abrir_imagem = tk.Button(frame_botoes, text="Abrir Imagem", command=edit_image.abrir_imagem)
botao_media = tk.Button(frame_botoes, text="Filtro Média", command=edit_image.media)
botao_gaus = tk.Button(frame_botoes, text="Filtro Gauss", command=edit_image.gauss)
botao_horizontal = tk.Button(frame_botoes, text="Filtro Horizontal", command=edit_image.horizontal)
botao_vertical = tk.Button(frame_botoes, text="Filtro Vertical", command=edit_image.vertical)
botao_laplaciano = tk.Button(frame_botoes, text="Filtro Laplaciano", command=edit_image.laplacian)
botao_boost = tk.Button(frame_botoes, text="Filtro Boost", command=edit_image.boost)
botao_selecao = tk.Button(frame_botoes, text="Selecionar Região", command=edit_image.iniciar_selecao)
botao_restaurar = tk.Button(frame_botoes, text="Imagem Original", command=edit_image.restaurar_imagem)
botao_desfazer = tk.Button(frame_botoes, text="Desfazer Alteração", command=edit_image.desfazer_alteracao)
botao_selecionar_cor = tk.Button(frame_botoes, text="Selecionar Cor", command=edit_image.regiao_clicada)
botao_detectar_cor = tk.Button(frame_botoes, text="Mudar Cor", command=edit_image.mudar_cor)

botao_abrir_imagem.grid(row=0, column=0)
botao_media.grid(row=0, column=1)
botao_gaus.grid(row=0, column=2)
botao_horizontal.grid(row=0, column=3)
botao_vertical.grid(row=0, column=4)
botao_laplaciano.grid(row=0, column=5)
botao_boost.grid(row=0, column=6)
botao_selecao.grid(row=0, column=7)
botao_restaurar.grid(row=0, column=8)
botao_desfazer.grid(row=0, column=9)
botao_selecionar_cor.grid(row=0, column=10)
botao_detectar_cor.grid(row=0, column=11)


frame_imagem.pack()

label_imagem.pack()

janela.mainloop()
