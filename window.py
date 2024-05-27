import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mplsoccer.pitch import Pitch
import pandas as pd
import re

# Variáveis para rastrear o estado do clique
clique_em_andamento = False
x_inicio, y_inicio, x_final, y_final = None, None, None, None
evento_atual = ""
coordenadas = []

# Variável para rastrear a linha selecionada na Treeview
linha_selecionada = None

# Variáveis para rastrear as seleções das ComboBoxes e o RadioButton
equipe_selecionada = ""
localizacao_selecionada = ""
zona_selecionada = ""
qualidade_selecionada = ""
tipo_selecionado = ""
jogador_selecionado =""

# Função para remover o último dado da lista
def remover_ultimo_dado():
    if coordenadas:
        coordenadas.pop()
        update_data_view()
        update_pitch()
        limpar_campos()

def on_combobox_options(event):
    update_localizacao_options(event)
    update_zona_options(event)
    update_qualidade_options(event)
    update_tipo_options(event)

def salvar_para_csv():
    if coordenadas:
        df = pd.DataFrame(coordenadas, columns=["ID", "Equipe", "Nº", "Jogador", "Tempo", "Evento", "Local", "Zona", "Qualidade", "Tipo", "X", "Y", "X2", "Y2"])
        df.to_csv("Dados coletados/dados_coletados.csv", index=False)
        messagebox.showinfo("Exportar", "Dados exportados para dados_coletados.csv com sucesso.")
    else:
        messagebox.showwarning("Exportar", "Não há dados para exportar.")

def definir_origem(origem):
    if "Casa" in jogador_selecionado.get():
        equipe_combo.set("Casa")
        equipe_combo.config(state="disabled")
    elif "Visitante" in jogador_selecionado.get():
        equipe_combo.set("Visitante")
        equipe_combo.config(state="disabled")
    else:
        equipe_combo.set("")

# Função para limpar os campos
def limpar_campos():
    jogador_selecionado.set("")
    equipe_combo.set("")
    evento_combo.set("")
    localizacao_combo.set("")
    zona_combo.set("")
    qualidade_combo.set("")
    tipo_combo.set("")
    tempo_selecionado.set(1)

def verificar_selecao_jogador():
    if equipe_combo["state"] == "disabled":
        messagebox.showinfo("Aviso", "Por favor, selecione um jogador antes de cadastrar um novo evento.")

def verificar_selecao_evento():
    if not evento_combo:
        messagebox.showinfo("Aviso", "Por favor, selecione um evento antes de cadastrar a coordenada.")

def evento_teste():
        selected_item = tree.focus()
        messagebox.showinfo(f"Item selecionado: {selected_item}")

def atualizar_combobox_state():
    if jogador_selecionado.get():  # Verifica se há um jogador selecionado
        equipe_combo["state"] = "readonly"  # Habilita a combobox
        evento_combo["state"] = "readonly"
        localizacao_combo["state"] = "readonly"
        zona_combo["state"] = "readonly"
        qualidade_combo["state"] = "readonly"
        tipo_combo["state"] = "readonly"
        ax.cla()  # Limpa o eixo do gráfico
        pitch.draw(ax=ax)  # Redesenha o campo de futebol
        canvas.draw()  # Atualiza o canvas        
    else:
        limpar_campos
        equipe_combo["state"] = "disabled"  # Desabilita a combobox
        evento_combo["state"] = "disabled"
        localizacao_combo["state"] = "disabled"
        zona_combo["state"] = "disabled"
        qualidade_combo["state"] = "disabled"
        tipo_combo["state"] = "disabled"

# Função para atualizar a seleção da ComboBox "Localização"
def update_equipe_selection(event):
    global equipe_selecionada
    equipe_selecionada = equipe_combo.get()

# Função para atualizar a seleção da ComboBox "Localização"
def update_localizacao_selection(event):
    global localizacao_selecionada
    localizacao_selecionada = localizacao_combo.get()

# Função para atualizar a seleção da ComboBox "Zona"
def update_zona_selection(event):
    global zona_selecionada
    zona_selecionada = zona_combo.get()

# Função para atualizar a seleção da ComboBox "Qualidade"
def update_qualidade_selection(event):
    global qualidade_selecionada
    qualidade_selecionada = qualidade_combo.get()

# Função para atualizar a seleção da ComboBox "Tipo"
def update_tipo_selection(event):
    global tipo_selecionado
    tipo_selecionado = tipo_combo.get()

# Função para atualizar a seleção do Jogador
def update_Jogador_selection(event):
    global jogador_selecionado
    jogador_selecionado = jogador_selecionado.get()

# Função para criar os radiobuttons com os nomes dos jogadores
def criar_radiobuttons(frame, jogadores, origem):
    for jogador in jogadores:
        id_jogador, nome_jogador = jogador
        texto_jogador = f"{id_jogador} - {nome_jogador} ({origem})"
        ttk.Radiobutton(frame, text=texto_jogador, variable=jogador_selecionado, value=texto_jogador, 
                        command=lambda: definir_origem(origem)).pack(padx=10, pady=2, anchor="w")
    
# Função para lidar com o início do clique no gráfico
def on_pitch_press(event):
    global clique_em_andamento, x_inicio, y_inicio, evento_atual
    x_inicio, y_inicio = event.xdata, event.ydata
    x_final, y_final = None, None
    clique_em_andamento = True
    evento_atual = evento_combo.get()
    ax.cla()
    pitch.draw(ax=ax)    
    if evento_atual in ["Finalização"]:
        ax.scatter(x_inicio, y_inicio, color='blue', marker='o')
    elif evento_atual in ["Passe"]:
        ax.scatter(x_inicio, y_inicio, color='lime')
    elif evento_atual in ["Defesa"]:
        ax.scatter(x_inicio, y_inicio, color='orange', marker='x', s=150)
    elif evento_atual in ["Comportamento"]:
        ax.scatter(x_inicio, y_inicio, color='yellow', marker='*', s=150)
    elif evento_atual in ["Condução"]:
        ax.scatter(x_inicio, y_inicio, color='white', marker='+')
    canvas.draw()

# Função para lidar com o movimento (arrastar) no gráfico
def on_pitch_motion(event):
    global x_final, y_final
    if clique_em_andamento:
        x_final, y_final = event.xdata, event.ydata
        ax.cla()
        pitch.draw(ax=ax)
        if evento_atual in ["Finalização"]:
            ax.scatter(x_inicio, y_inicio, color='blue', marker='o')
        elif evento_atual in ["Passe"]:
            ax.scatter(x_inicio, y_inicio, color='lime', marker='o')
        elif evento_atual in ["Defesa"]:
            ax.scatter(x_inicio, y_inicio, color='orange', marker='x', s=150)
        elif evento_atual in ["Comportamento"]:
            ax.scatter(x_inicio, y_inicio, color='yellow', marker='*', s=150)
        elif evento_atual in ["Condução"]:
            ax.scatter(x_inicio, y_inicio, color='white', marker='s')
        if x_final is not None and y_final is not None:
            ax.scatter(x_final, y_final, s=150, color='white', marker='+')
            if evento_atual in ["Finalização"]:
                ax.plot([x_inicio, x_final], [y_inicio, y_final], color='blue', marker='o')        
            elif   evento_atual in ["Passe"]:
                ax.plot([x_inicio, x_final], [y_inicio, y_final], color='lime', marker='o')                                
            elif  evento_atual in ["Condução"]:
                ax.plot([x_inicio, x_final], [y_inicio, y_final], color='white', marker='+')
        if evento_atual in ["Defesa"]:
            ax.scatter(x_inicio, y_inicio, color='orange', marker='x', s=100)
        elif evento_atual in ["Comportamento"]:
            ax.scatter(x_inicio, y_inicio, color='yellow', marker='*', s=150)
        canvas.draw()

# Função para atualizar o gráfico
def update_pitch():
    ax.cla()
    pitch.draw(ax=ax)
    for coord in coordenadas:
        coord_formatado = formatar_coordenadas(coord)
        x_ini, y_ini, x_fin, y_fin = coord_formatado[9:13]  # Ajuste os índices com base na estrutura da sua lista
        if coord_formatado[4] in ["Comportamento"]:
            ax.scatter(x_ini, y_ini, color='yellow', marker='*', s=150)
        elif coord_formatado[4] in ["Defesa"]:
            ax.scatter(x_ini, y_ini, color='orange', marker='x', s=150)
        else:
            if x_ini is not None and y_ini is not None:
                ax.scatter(x_ini, y_ini, s=100)
                if x_fin is not None and y_fin is not None:
                    ax.scatter(x_fin, y_fin, s=100)
                    if coord_formatado[4] in ["Finalização"]:
                        ax.plot([x_ini, x_fin], [y_ini, y_fin], color='blue', marker='o')
                    elif coord_formatado[4] in ["Passe"]:
                        ax.plot([x_ini, x_fin], [y_ini, y_fin], color='lime', marker='o')               
    canvas.draw()

# Função para lidar com o fim do clique no gráfico
def on_pitch_release(event):
    global clique_em_andamento
    nome_numero = jogador_selecionado.get().split('-')
    # Extraia o número e o nome
    numero = nome_numero[0].strip()
    nome = nome_numero[1].split('(')[0].strip() #(ignorando o que está dentro dos parênteses)
    if clique_em_andamento:
        evento = evento_combo.get()
        x_ini, y_ini, x_fin, y_fin = x_inicio, y_inicio, x_final, y_final
        if evento in ["Defesa", "Comportamento"]:
            coordenadas.append([len(coordenadas) + 1, equipe_combo.get(), numero, nome, tempo_selecionado.get(), evento, localizacao_selecionada, zona_selecionada, qualidade_selecionada, tipo_selecionado, x_ini, y_ini, None, None])
        else:
            coordenadas.append([len(coordenadas) + 1, equipe_combo.get(), numero, nome, tempo_selecionado.get(), evento, localizacao_selecionada, zona_selecionada, qualidade_selecionada, tipo_selecionado, x_ini, y_ini, x_fin, y_fin])
        update_data_view()
        clique_em_andamento = False        

# Função para atualizar a visualização da tabela e do gráfico
def update_data_view():
    tree.delete(*tree.get_children())
    for coord in coordenadas:
        coord_formatado = formatar_coordenadas(coord)
        tree.insert("", "end", values=tuple(coord))
    limpar_campos()  # Chama a função para limpar os campos

# Para formatar os valores de X e Y com duas casas decimais
def formatar_coordenadas(coord):
    for i in range(len(coord)):
        if (i>0) and (isinstance(coord[i], (int, float))):
            coord[i] = "{:.2f}".format(coord[i])
    return coord

# Função para mostrar a coordenada no gráfico quando uma linha é selecionada na Treeview
def ver_coordenadas(event):
    global linha_selecionada
    item = tree.selection()[0]
    linha_selecionada = int(item) - 1
    update_pitch()
    if linha_selecionada >= 0 and linha_selecionada < len(coordenadas):
        coord = coordenadas[linha_selecionada]
        x_ini, y_ini, x_fin, y_fin = coord[9:13]  # Ajuste os índices com base na estrutura da sua lista
        print('x_ini: ' + x_ini)
        print('y_ini: ' + y_ini)
        print('x_fin: ' + x_fin)
        print('y_fin: ' + y_fin)     
        if x_ini is not None and y_ini is not None:
            if x_fin is not None and y_fin is not None:
                print(f"Coordenadas: X1={x_ini}, Y1={y_ini}, X2={x_fin}, Y2={y_fin}")
            else:
                print(f"Coordenadas: X={x_ini}, Y={y_ini}")
        else:
            print(f"Coordenadas: Não disponíveis")


# Função para atualizar as opções do ComboBox "Localização" com base no evento selecionado
def update_localizacao_options(event):
    evento = evento_combo.get()
    if evento:
        localizacao_combo['values'] = [
            "Intermediária", "Centro", "Grande área", "Pqna área", "Corredor direito", "Corredor esquerdo"
        ]
    else:
        localizacao_combo.set("")
        localizacao_combo['values'] = []  

# Função para atualizar as opções do ComboBox "Zona" com base no evento selecionado
def update_zona_options(event):
    evento = evento_combo.get()
    if evento:
        zona_combo['values'] = [
            "Defensiva", "Ofensiva"
        ]
    else:
        zona_combo.set("")
        zona_combo['values'] = []
        

# Função para atualizar as opções do ComboBox "Qualidade" com base no evento selecionado
def update_qualidade_options(event):
    evento = evento_combo.get()
    if evento == "Finalização":
        qualidade_combo['values'] = [
            "Ótima", "Boa", "Ruim", "Pessíma", "Gol"
        ]
    elif evento == "Defesa":
        qualidade_combo['values'] = ["Ótimo", "Bom", "Ruim", "Pessímo", "Gol contra"]
    else:
        qualidade_combo['values'] = ["Ótimo", "Bom", "Ruim", "Pessímo"]

def update_tipo_options(event):
    evento = evento_combo.get()
    if evento == "Finalização":
        tipo_combo['values'] = [
            "Normal", "Colocada", "Cabeceio", "Voleio", "Chutão",
              "Cavadinha", "Bicicleta", "Bola Parada", "Forte", "Falha"
        ]
    elif evento == "Passe":
        tipo_combo['values'] = [
            "Rasteiro", "De cabeça", "Enfiada", "Enfiada por cima (de cabeça)", "Bola Parada",
            "Cruzamento (1ª trave)", "Cruzamento (2ª trave)", "Passe Importante", "De primeira",
            "Toco y me voy", "Na ponta", "Quebra-linhas", "Recuando", "Escanteiro", "Invertendo",
            "Lançamento"
        ]
    elif evento == "Defesa":
        tipo_combo['values'] = [
            "Normal", "Carrinho", "Interceptação", "Chutões", "Bloqueios", "Dividida",
			"Mão trocada", "Espalmando para os lados", "Espalmando para frente", "Fechando a linha de passe",
            "Soco na bola", "Na ponta dos dedos", "Com os pés", "No reflexo", "Rebote", "Falha", "Corte", "Falta", "Falta tática"
        ]
    elif evento == "Comportamento":
        tipo_combo['values'] = [
            	 "Reclamação com arbitragem", "Reclamação com companheiro", "Reclamação com a comissão", "Simulação", "Pressão",
                 "Reclamação com adversário", "Cartão Amarelo", "Cartão Vermelho", "Tomada de decisão", "Infiltração", "Cobertura",
                 "Faltas cometida", "Penalty cometido", "Impedimento", "Orientando o companheiro", "Conversa com a comissão", "Domínio",
                 "Domínio com drible", "Pedindo a bola", "Opção para passe", "Falta sofrida", "Posicionamento"
        ]
    elif evento == "Condução":
        tipo_combo['values'] = [
            	"Normal", "Superando oponentes na velocidade", "Perda da posse de bola",
                "Superando oponentes com fintas", "Adiantadas", "Contra ataque"
        ]
    else:
        tipo_combo.set("")
        tipo_combo['values'] = []

# Cria uma janela
janela = tk.Tk()
janela.title("Coletor de Eventos")
janela.geometry('1920x1080')
janela.state('zoomed')
# Defina a resolução da tela
largura_total = 1920
altura_total = 1080

# Calcula as dimensões dos frames
largura_frame_time = largura_total * 0.3
altura_frame_time = altura_total
largura_frame_formulario1 = largura_total * 0.2
altura_frame_formulario1 = altura_total * 0.10
largura_frame_formulario2 = largura_total * 0.2
altura_frame_formulario2 = altura_total * 0.10
largura_frame_visitante = largura_total * 0.3
altura_frame_visitante = altura_total
largura_frame_visualizacao = largura_total * 0.4
altura_frame_visualizacao = altura_total * 0.55
largura_frame_tree = largura_total * 0.4
altura_frame_tree = altura_total * 0.25


# Crie os frames com as dimensões desejadas
frame_time_casa = tk.Frame(janela, width=largura_frame_time, height=altura_frame_time, padx=5, pady=5)
frame_time_visitante = tk.Frame(janela, width=largura_frame_visitante, height=altura_frame_visitante, padx=5, pady=5)
frame_visualizacao = tk.Frame(janela, width=largura_frame_visualizacao, height=altura_frame_visualizacao, padx=5, background='white')
frame_tree = tk.Frame(janela, width=largura_frame_tree, height=altura_frame_tree, padx=5, background='white')
frame_buttons = tk.Frame(janela, width=24, height=6, padx=5, background='white')

# Posicione os frames na janela usando pack
frame_time_casa.pack(side="left", fill="both")
frame_time_visitante.pack(side="right", fill="both")

# Crie um frame que contém frame_formulario e frame_visualizacao
frame_top = tk.Frame(width=largura_frame_formulario1, height=altura_frame_formulario1, background='white')
frame_top.pack(side="top", fill="both", expand=True)
frame_formulario1 = tk.Frame(frame_top, width=largura_frame_formulario1, height=altura_frame_formulario1, padx=5, pady=5, background='white')
frame_formulario2 = tk.Frame(frame_top, width=largura_frame_formulario2, height=altura_frame_formulario2, padx=5, pady=5, background='white')
frame_formulario1.pack(side="left", fill="both", expand=True)
frame_formulario2.pack(side="right", fill="both", expand=True)
frame_formulario1.pack_propagate(False)
frame_formulario2.pack_propagate(False)
frame_top.pack_propagate(False)

frame_central = tk.Frame(janela)
frame_visualizacao.pack(side="top", fill="both")
frame_tree.pack(side="top", fill="both")
frame_buttons.pack(side="bottom", fill="both")

# Configura o redimensionamento dos frames
frame_top.pack_propagate(False)
frame_visualizacao.pack_propagate(False)
frame_tree.pack_propagate(False)

# Organiza o frame_central no meio
frame_central.pack(side="left", fill="y")

# Leitura dos dados do arquivo CSV
dados_casa = pd.read_csv("Dados jogadores/Dados_jogadores_COR.csv")
dados_visitante = pd.read_csv("Dados jogadores/Dados_jogadores_CAM.csv")

# Ordena os dados pelo ID e Status
dados_ord_casa = dados_casa.sort_values(by=["ID", "Status"])
dados_ord_visitante = dados_visitante.sort_values(by=["ID", "Status"])

# Selecionar as colunas "ID" e "Player_name" e criar a lista
jogadores_casa = dados_ord_casa[["ID","Player_name"]].values.tolist()
jogadores_visitante = dados_ord_visitante[["ID","Player_name"]].values.tolist()

label_time_casa = tk.Label(frame_time_casa, text="Time Casa", font= ctk.CTkFont(size=15, weight='bold' ))
label_time_casa.pack()
label_time_visitante = tk.Label(frame_time_visitante, text="Time Visitante", font= ctk.CTkFont(size=15, weight='bold' ))
label_time_visitante.pack()

# Criar o label para os escudos
escudo_casa = PhotoImage(file='Escudos/Corinthians.png')
escudo_casa = escudo_casa.subsample(7, 7)
label_escudo_casa = ctk.CTkLabel(frame_time_casa, image=escudo_casa, text='')
label_escudo_casa.pack()
# Visitante
escudo_visitante = PhotoImage(file='Escudos/Atlético Mineiro.png')
escudo_visitante = escudo_visitante.subsample(7, 7)
label_escudo_visitante = ctk.CTkLabel(frame_time_visitante, image=escudo_visitante, text='')
label_escudo_visitante.pack()

# Crie um label para "Time"
label_team = ttk.Label(frame_time_casa, text=dados_casa["Team"].values[0] +" - "+dados_casa["Alias"].values[0])
label_team.pack(side="top")
label_team = ttk.Label(frame_time_visitante, text=dados_visitante["Team"].values[0] +" - "+dados_visitante["Alias"].values[0])
label_team.pack(side="top")

# Crie um label para "Técnico"
label_manager_casa= ttk.Label(frame_time_casa, text=dados_casa["Manager_name"].values[0])
label_manager_casa.pack(side="top", pady=5) 
label_manager_visitante= ttk.Label(frame_time_visitante, text=dados_visitante["Manager_name"].values[0])
label_manager_visitante.pack(side="top", pady=5)

jogador_selecionado = tk.StringVar()
# Variável para acompanhar o jogador selecionado
jogador_selecionado.trace("w", lambda *args: atualizar_combobox_state())

# Crie os radiobuttons com os nomes dos jogadores
criar_radiobuttons(frame_time_casa, jogadores_casa, 'Casa')
criar_radiobuttons(frame_time_visitante, jogadores_visitante, 'Visitante')

equipe_selecionada = tk.StringVar()
# Trace a variável selected_player para chamar a função definir_origem
jogador_selecionado.trace("w", lambda *args: definir_origem("Casa"))

# Crie o formulário com as opções 
equipe_label = tk.Label(frame_formulario1, text="Equipe:", font= ctk.CTkFont(size=12, weight='bold' ), background='white')
equipe_label.pack()
equipe_combo = ttk.Combobox(frame_formulario1, values=["Casa", "Visitante"], width=25, textvariable=equipe_selecionada)
equipe_combo["state"] = "readonly"
equipe_combo.pack()

evento_label = tk.Label(frame_formulario1, text="Evento:", font= ctk.CTkFont(size=12, weight='bold' ), background='white')
evento_label.pack()
evento_combo = ttk.Combobox(frame_formulario1, values=["Finalização", "Passe", "Defesa", "Comportamento", "Condução"], width=25 )
evento_combo["state"] = "readonly"
evento_combo.pack()
evento_combo.bind("<<Button1>>", atualizar_combobox_state)
evento_combo.bind("<<ComboboxSelected>>", on_combobox_options)

# Combo "Localização" para o evento "Finalização"
localizacao_label = tk.Label(frame_formulario1, text="Local:", font= ctk.CTkFont(size=12, weight='bold' ), background='white')
localizacao_label.pack()
localizacao_combo = ttk.Combobox(frame_formulario1, values=[], width=25)
localizacao_combo["state"] = "readonly"
localizacao_combo.pack()

# Combo "Zona" para o evento "Passe"
zona_label = tk.Label(frame_formulario2, text="Zona:", font= ctk.CTkFont(size=12, weight='bold' ), background='white')
zona_label.pack()
zona_combo = ttk.Combobox(frame_formulario2, values=[], width=25)
zona_combo["state"] = "readonly"
zona_combo.pack()

# Combo "Qualidade" para os eventos "Finalização" e "Passe"
qualidade_label = tk.Label(frame_formulario2, text="Qualidade:", font= ctk.CTkFont(size=12, weight='bold' ), background='white')
qualidade_label.pack()
qualidade_combo = ttk.Combobox(frame_formulario2, values=[], width=25)
qualidade_combo["state"] = "readonly"
qualidade_combo.pack()

# Combo "Tipo" para os eventos "Finalização" e "Passe"
tipo_label = tk.Label(frame_formulario2, text="Tipo:", font= ctk.CTkFont(size=12, weight='bold' ), background='white')
tipo_label.pack()
tipo_combo = ttk.Combobox(frame_formulario2, values=[], width=25)
tipo_combo["state"] = "readonly"
tipo_combo.pack()

# Cria o botão "Exportar"
botao_exportar = ctk.CTkButton(frame_buttons, text="Exportar", command=salvar_para_csv, height=6, width=12)
botao_exportar.pack(side=ctk.RIGHT)

# Cria um botão para deletar a última coordenada inserida
botao_deletar = ctk.CTkButton(frame_buttons, text="Deletar", command=remover_ultimo_dado, height=6, width=12)
botao_deletar.pack(side=ctk.RIGHT)

#Criar o radioButtom para selecinar o tempo da partida
# Variável para rastrear a seleção do radiobutton
tempo_selecionado = tk.StringVar()
# Crie os radiobuttons
radio_primeiro_tempo = tk.Radiobutton(frame_visualizacao, text="Primeiro tempo", variable=tempo_selecionado, value=1, background='white').pack(side=ctk.TOP)
radio_segundo_tempo = tk.Radiobutton(frame_visualizacao, text="Segundo tempo", variable=tempo_selecionado, value=2, background='white').pack(side=ctk.TOP)
tempo_selecionado.set(1) # 1º Tempo selecionado como padrão

# Inicializa uma lista para armazenar as coordenadas
coordenadas = []

# Cria o gráfico de campo de futebol (pitch)
pitch = Pitch(pitch_color='grass', line_color='white', stripe=True, axis=False, 
              label=False, positional=True, positional_alpha=0, goal_type= 'box', corner_arcs=True,
              pad_top=5, pad_bottom=5, pad_left=5, pad_right=5)
fig, ax = pitch.draw()

# Adiciona o gráfico à janela usando FigureCanvasTkAgg
canvas = FigureCanvasTkAgg(fig, master=frame_visualizacao)
canvas.get_tk_widget().config(width=largura_frame_visualizacao*0.5, height=altura_frame_visualizacao*0.5)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Adiciona eventos de clique, arrastar e soltar ao gráfico
canvas.mpl_connect('button_press_event', on_pitch_press)
canvas.mpl_connect('motion_notify_event', on_pitch_motion)
canvas.mpl_connect('button_release_event', on_pitch_release)

columns = ("ID", "Equipe","Nº","Jogador", "Tempo", "Evento", "Local", "Zona", "Qualidade", "Tipo", "X", "Y", "X2", "Y2")
tree = ttk.Treeview(frame_tree, columns=columns)
tree.bind("<<TreeviewSelected>>", ver_coordenadas)


localizacao_combo.bind("<<ComboboxSelected>>", update_localizacao_selection)
zona_combo.bind("<<ComboboxSelected>>", update_zona_selection)
qualidade_combo.bind("<<ComboboxSelected>>", update_qualidade_selection)
tipo_combo.bind("<<ComboboxSelected>>", update_tipo_selection)

equipe_combo.bind("<FocusIn>", lambda e: verificar_selecao_jogador())
evento_combo.bind("<FocusIn>", lambda e: verificar_selecao_jogador())
tipo_combo.bind("<FocusIn>", lambda e: verificar_selecao_jogador())
localizacao_combo.bind("<FocusIn>", lambda e: verificar_selecao_jogador())
zona_combo.bind("<FocusIn>", lambda e: verificar_selecao_jogador())
qualidade_combo.bind("<FocusIn>", lambda e: verificar_selecao_jogador())

# Mudei a abordagem para fixar a largura por 
tree.column("#0", width=0, minwidth=0, stretch=False)
tree.column("ID", anchor="center", width=10, minwidth=10)
tree.column("Equipe", anchor="center", width=35, minwidth=30)
tree.column("Nº", anchor="center", width=10, minwidth=10)
tree.column("Jogador", anchor="center", width=65, minwidth=50)
tree.column("Tempo", anchor="center", width=15, minwidth=10)
tree.column("Evento", anchor="center", width=50, minwidth=50)
tree.column("Local", anchor="center", width=55, minwidth=45)
tree.column("Zona", anchor="center", width=40, minwidth=40)
tree.column("Qualidade", anchor="center", width=45, minwidth=45)
tree.column("Tipo", anchor="center", width=52, minwidth=50)
tree.column("X", anchor="center", width=12, minwidth=10)
tree.column("Y", anchor="center", width=12, minwidth=10)
tree.column("X2", anchor="center", width=12, minwidth=10)
tree.column("Y2", anchor="center", width=12, minwidth=10)

tree.heading("#0", text="")
tree.heading("ID", anchor="center", text="ID")
tree.heading("Equipe", anchor="center", text="Equipe")
tree.heading("Nº", anchor="center", text="Nº")
tree.heading("Jogador", anchor="center", text="Jogador")
tree.heading("Tempo", anchor="center", text="Tempo") 
tree.heading("Evento", anchor="center", text="Evento")
tree.heading("Local", anchor="center", text="Local")
tree.heading("Zona", anchor="center", text="Zona")
tree.heading("Qualidade", anchor="center", text="Qualidade")
tree.heading("Tipo", anchor="center", text="Tipo")
tree.heading("X", anchor="center", text="X") 
tree.heading("Y", anchor="center", text="Y") 
tree.heading("X2", anchor="center", text="X2")
tree.heading("Y2", anchor="center", text="Y2")

tree.bind("<<TreeViewSelected>>", evento_teste)

tree.pack(fill="both", expand=True)

limpar_campos()

janela.mainloop()  