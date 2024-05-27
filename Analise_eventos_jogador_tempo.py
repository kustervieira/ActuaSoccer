import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
import seaborn as sns

# Ler os dados
df = pd.read_csv('Dados coletados/dados_coletados_COR_CAM_44_5.csv')

global nome_jogador

#print(df.dtypes)
def criar_grafico():
    global fig, ax 
    fig,ax = plt.subplots(figsize=(13.5, 8))
    fig.set_facecolor('#22312b')
    ax.patch.set_facecolor('#22312b')
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b',  line_color='#c7d5cc')
    pitch.draw(ax=ax)

def plot_heatmap(heat_df, ax):
    heat_df = heat_df
    #heat_df = heat_df.loc[(heat_df['teamId']==teamId) & (heat_df['type']==p_type)]
    kde = sns.kdeplot(
    x=heat_df.X, y=heat_df.Y, data = heat_df,
    fill=True,
    cmap='magma',
    #alpha=.05,
    ax=ax
    )

num_jogador=44 # 44 Moscardo, 5 Fausto

# Filtrando o data frame
df_passes_t1 = df.loc[(df['Evento']=='Passe') & (df['Nº']==num_jogador) & (df['Tempo']==1)].reset_index(drop=True)
df_passes_t2 = df.loc[(df['Evento']=='Passe') & (df['Nº']==num_jogador) & (df['Tempo']==2)].reset_index(drop=True)
df_finalizacao_t1 = df.loc[(df['Evento']=='Finalização') & (df['Nº']==num_jogador) & (df['Tempo']==1)].reset_index(drop=True)
df_finalizacao_t2 = df.loc[(df['Evento']=='Finalização') & (df['Nº']==num_jogador) & (df['Tempo']==2)].reset_index(drop=True)
df_defesa_t1 = df.loc[(df['Evento']=='Defesa') & (df['Nº']==num_jogador) & (df['Tempo']==1)].reset_index(drop=True)
df_defesa_t2 = df.loc[(df['Evento']=='Defesa') & (df['Nº']==num_jogador) & (df['Tempo']==2)].reset_index(drop=True)
df_comportamento_t1 = df.loc[(df['Evento']=='Comportamento') & (df['Nº']==num_jogador) & (df['Tempo']==1)].reset_index(drop=True)
df_comportamento_t2 = df.loc[(df['Evento']=='Comportamento') & (df['Nº']==num_jogador) & (df['Tempo']==2)].reset_index(drop=True)
df_conducao_t1 = df.loc[(df['Evento']=='Condução') & (df['Nº']==num_jogador) & (df['Tempo']==1)].reset_index(drop=True)
df_conducao_t2 = df.loc[(df['Evento']=='Condução') & (df['Nº']==num_jogador) & (df['Tempo']==2)].reset_index(drop=True)


for i in range(len(df_passes_t1['Jogador'])):
    nome_jogador = df_passes_t1['Jogador'][i]

#print(nome_jogador)
#
### INICIO #####
#
criar_grafico()

plot_heatmap(df, ax)

#kde = sns.kdeplot(df['X'], df['Y'], shade= True, shade_lowest=False, alpha=.5, n_levels=10, cmap= 'magma')

for x in range(len(df_passes_t1['X'])):
    if df_passes_t1['Qualidade'].loc[x] not in ["Ruim", "Péssima"] and df_passes_t1['Nº'].loc[x]==num_jogador:
        plt.plot((df_passes_t1['X'][x], df_passes_t1['X2'][x]),(df_passes_t1['Y'][x], df_passes_t1['Y2'][x]),color='lime')
        plt.scatter(df_passes_t1['X'][x], df_passes_t1['Y'][x], color='lime')
    if df_passes_t1['Qualidade'].loc[x] in ["Ruim", "Péssima"]and df_passes_t1['Nº'].loc[x]==num_jogador:
        plt.plot((df_passes_t1['X'][x], df_passes_t1['X2'][x]),(df_passes_t1['Y'][x], df_passes_t1['Y2'][x]),color='red')
        plt.scatter(df_passes_t1['X'][x], df_passes_t1['Y'][x], color='red')

for x in range(len(df_finalizacao_t1['X'])):
    if df_finalizacao_t1['Qualidade'].loc[x] not in ["Ruim", "Péssima"] and df_finalizacao_t1['Nº'].loc[x]==num_jogador:
        plt.plot((df_finalizacao_t1['X'][x], df_finalizacao_t1['X2'][x]),(df_finalizacao_t1['Y'][x], df_finalizacao_t1['Y2'][x]),color='blue', marker='o')
        plt.scatter(df_finalizacao_t1['X'][x], df_finalizacao_t1['Y'][x], color='blue')
    if df_finalizacao_t1['Qualidade'].loc[x] in ["Ruim", "Péssima"]and df_finalizacao_t1['Nº'].loc[x]==num_jogador:
        plt.plot((df_finalizacao_t1['X'][x], df_finalizacao_t1['X2'][x]),(df_finalizacao_t1['Y'][x], df_finalizacao_t1['Y2'][x]),color='orange', marker='o')
        plt.scatter(df_finalizacao_t1['X'][x], df_finalizacao_t1['Y'][x], color='red')

for x in range(len(df_defesa_t1['X'])):
    if df_defesa_t1['Qualidade'].loc[x] not in ["Ruim", "Péssima"] and df_defesa_t1['Nº'].loc[x]==num_jogador:
        #plt.plot((df_passes_t1['X'][x], df_passes_t1['X2'][x]),(df_passes_t1['Y'][x], df_passes_t1['Y2'][x]),color='lime')
        plt.scatter(df_defesa_t1['X'][x], df_defesa_t1['Y'][x], color='orange', marker='x', s=80)
    if df_defesa_t1['Qualidade'].loc[x] in ["Ruim", "Péssima"]and df_defesa_t1['Nº'].loc[x]==num_jogador:
        #plt.plot((df_passes_t1['X'][x], df_passes_t1['X2'][x]),(df_passes_t1['Y'][x], df_passes_t1['Y2'][x]),color='red')
        plt.scatter(df_defesa_t1['X'][x], df_defesa_t1['Y'][x], color='red', marker='x', s=80)

for x in range(len(df_comportamento_t1['X'])):
    if df_comportamento_t1['Qualidade'].loc[x] not in ["Ruim", "Péssima"] and df_comportamento_t1['Nº'].loc[x]==num_jogador:
        #plt.plot((df_passes_t1['X'][x], df_passes_t1['X2'][x]),(df_passes_t1['Y'][x], df_passes_t1['Y2'][x]),color='lime')
        plt.scatter(df_comportamento_t1['X'][x], df_comportamento_t1['Y'][x], color='yellow', marker='*', s=80)
    if df_comportamento_t1['Qualidade'].loc[x] in ["Ruim", "Péssima"]and df_comportamento_t1['Nº'].loc[x]==num_jogador:
        #plt.plot((df_passes_t1['X'][x], df_passes_t1['X2'][x]),(df_passes_t1['Y'][x], df_passes_t1['Y2'][x]),color='red')
        plt.scatter(df_comportamento_t1['X'][x], df_comportamento_t1['Y'][x], color='red', marker='*', s=80)

for x in range(len(df_conducao_t1['X'])):
    if df_conducao_t1['Qualidade'].loc[x] not in ["Ruim", "Péssima"] and df_conducao_t1['Nº'].loc[x]==num_jogador:
        plt.plot((df_conducao_t1['X'][x], df_conducao_t1['X2'][x]),(df_conducao_t1['Y'][x], df_conducao_t1['Y2'][x]),color='lime')
        plt.scatter(df_conducao_t1['X'][x], df_conducao_t1['Y'][x], color='blue')
    if df_conducao_t1['Qualidade'].loc[x] in ["Ruim", "Péssima"]and df_conducao_t1['Nº'].loc[x]==num_jogador:
        plt.plot((df_conducao_t1['X'][x], df_conducao_t1['X2'][x]),(df_conducao_t1['Y'][x], df_conducao_t1['Y2'][x]),color='red')
        plt.scatter(df_conducao_t1['X'][x], df_conducao_t1['Y'][x], color='red')

plt.title('Mapa dos passes: ' + nome_jogador +'\n COR x CAM 1º tempo', color='w', size=15)
#plt.legend(['Sentido ataque -->'], loc='upper center', bbox_to_anchor=(0.5, -0.1))
legend = plt.legend(['Sentido ataque -->'], loc='upper center', bbox_to_anchor=(0.5, 0.05), handlelength=0)
# Remover o fundo
legend.get_frame().set_facecolor('None')
legend.get_frame().set_linewidth(0)
# Configurar a cor do texto para branco
for text in legend.get_texts():
    text.set_color('white')
    text.set_fontsize(15.0)

plt.show()

# Limpar o gráfico atual para a nova plotagem
ax.clear()
criar_grafico()

for x in range(len(df_passes_t2['X'])):
    if df_passes_t2['Qualidade'].loc[x] not in ["Ruim", "Péssima"] and df_passes_t2['Nº'].loc[x]==num_jogador:
        plt.plot((df_passes_t2['X'][x], df_passes_t2['X2'][x]),(df_passes_t2['Y'][x], df_passes_t2['Y2'][x]),color='lime')
        plt.scatter(df_passes_t2['X'][x], df_passes_t2['Y'][x], color='lime')
    if df_passes_t2['Qualidade'].loc[x] in ["Ruim", "Péssima"]and df_passes_t2['Nº'].loc[x]==num_jogador:
        plt.plot((df_passes_t2['X'][x], df_passes_t2['X2'][x]),(df_passes_t2['Y'][x], df_passes_t2['Y2'][x]),color='red')
        plt.scatter(df_passes_t2['X'][x], df_passes_t2['Y'][x], color='red')

for x in range(len(df_finalizacao_t2['X'])):
    if df_finalizacao_t2['Qualidade'].loc[x] not in ["Ruim", "Péssima"] and df_finalizacao_t2['Nº'].loc[x]==num_jogador:
        plt.plot((df_finalizacao_t2['X'][x], df_finalizacao_t2['X2'][x]),(df_finalizacao_t2['Y'][x], df_finalizacao_t2['Y2'][x]),color='blue', marker='o')
        plt.scatter(df_finalizacao_t2['X'][x], df_finalizacao_t2['Y'][x], color='blue')
    if df_finalizacao_t2['Qualidade'].loc[x] in ["Ruim", "Péssima"]and df_finalizacao_t2['Nº'].loc[x]==num_jogador:
        plt.plot((df_finalizacao_t2['X'][x], df_finalizacao_t2['X2'][x]),(df_finalizacao_t2['Y'][x], df_finalizacao_t2['Y2'][x]),color='red', marker='o')
        plt.scatter(df_finalizacao_t2['X'][x], df_finalizacao_t2['Y'][x], color='red')

for x in range(len(df_defesa_t2['X'])):
    if df_defesa_t2['Qualidade'].loc[x] not in ["Ruim", "Péssima"] and df_defesa_t2['Nº'].loc[x]==num_jogador:
        #plt.plot((df_passes_t2['X'][x], df_passes_t2['X2'][x]),(df_passes_t2['Y'][x], df_passes_t2['Y2'][x]),color='lime')
        plt.scatter(df_defesa_t2['X'][x], df_defesa_t2['Y'][x], color='orange', marker='x', s=80)
    if df_defesa_t2['Qualidade'].loc[x] in ["Ruim", "Péssima"]and df_defesa_t2['Nº'].loc[x]==num_jogador:
        #plt.plot((df_passes_t2['X'][x], df_passes_t2['X2'][x]),(df_passes_t2['Y'][x], df_passes_t2['Y2'][x]),color='red')
        plt.scatter(df_defesa_t2['X'][x], df_defesa_t2['Y'][x], color='red', marker='x', s=80)

for x in range(len(df_comportamento_t2['X'])):
    if df_comportamento_t2['Qualidade'].loc[x] not in ["Ruim", "Péssima"] and df_comportamento_t2['Nº'].loc[x]==num_jogador:
        #plt.plot((df_passes_t2['X'][x], df_passes_t2['X2'][x]),(df_passes_t2['Y'][x], df_passes_t2['Y2'][x]),color='lime')
        plt.scatter(df_comportamento_t2['X'][x], df_comportamento_t2['Y'][x], color='yellow', marker='*', s=80)
    if df_comportamento_t2['Qualidade'].loc[x] in ["Ruim", "Péssima"]and df_comportamento_t2['Nº'].loc[x]==num_jogador:
        #plt.plot((df_passes_t2['X'][x], df_passes_t2['X2'][x]),(df_passes_t2['Y'][x], df_passes_t2['Y2'][x]),color='red')
        plt.scatter(df_comportamento_t2['X'][x], df_comportamento_t2['Y'][x], color='red', marker='*', s=80)

for x in range(len(df_conducao_t2['X'])):
    if df_conducao_t2['Qualidade'].loc[x] not in ["Ruim", "Péssima"] and df_conducao_t2['Nº'].loc[x]==num_jogador:
        plt.plot((df_conducao_t2['X'][x], df_conducao_t2['X2'][x]),(df_conducao_t2['Y'][x], df_conducao_t2['Y2'][x]),color='lime')
        plt.scatter(df_conducao_t2['X'][x], df_conducao_t2['Y'][x], color='lime')
    if df_conducao_t2['Qualidade'].loc[x] in ["Ruim", "Péssima"]and df_conducao_t2['Nº'].loc[x]==num_jogador:
        plt.plot((df_conducao_t2['X'][x], df_conducao_t2['X2'][x]),(df_conducao_t2['Y'][x], df_conducao_t2['Y2'][x]),color='red')
        plt.scatter(df_conducao_t2['X'][x], df_conducao_t2['Y'][x], color='red')

plt.title('Mapa dos passes: ' + nome_jogador +'\n COR x CAM 2º tempo', color='w', size=15)
legend = plt.legend(['<-- Sentido ataque'], loc='upper center', bbox_to_anchor=(0.5, 0.05), handlelength=0)
# Remover o fundo
legend.get_frame().set_facecolor('None')
legend.get_frame().set_linewidth(0)
# Configurar a cor do texto para branco
for text in legend.get_texts():
    text.set_color('white')
    text.set_fontsize(15.0)

plt.show()

#
### FIM  #####
##
