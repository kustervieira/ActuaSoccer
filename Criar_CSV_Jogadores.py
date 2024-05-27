import csv

#
#### TIME CASA #####
#

# Dados dos jogadores
titulares_home = [
    12, "Cassio",
    3, "Lucas Verissimo",
    4, "Gil",
    21, "Matheus Bidu",
    23, "Fagner",
    7, "Maycon",
    8, "Renato Augusto",
    11, "Angel Romero",
    20, "Giuliano",
    44, "Gabriel Moscardo",
    9, "Yuri Alberto",
]

banco_home = [
    2, "Rafael Ramos",
    10, "Matias Rojas",
    14, "Caetano",
    22, "Carlos Miguel",
    24, "Victor Cantillo",
    25, "Bruno Mendez",
    27, "Pedro Henrique",
    29, "Roni",
    30, "Matheus Araujo",
    33, "Ruan Oliveira",
    36, "Wesley Gassova",
    41, "Felipe Augusto",
]

tecnico_home = "Luiz Antonio Venker de Menezes"
time_home = "Corinthians"
abreviatura_home = "COR"

# Criar lista de jogadores com status (titular ou banco)
jogadores_home = []

for i in range(0, len(titulares_home), 2):
    jogador_id = titulares_home[i]
    jogador_nome = titulares_home[i + 1]
    jogadores_home.append([jogador_id, jogador_nome, tecnico_home, time_home, abreviatura_home, 1])

for i in range(0, len(banco_home), 2):
    jogador_id = banco_home[i]
    jogador_nome = banco_home[i + 1]
    jogadores_home.append([jogador_id, jogador_nome, tecnico_home, time_home, abreviatura_home, 2])

# Escrever os dados em um arquivo CSV
with open('Dados Jogadores/Dados_jogadores_'+abreviatura_home+'.csv', mode='w', newline='') as arquivo_csv:
    writer = csv.writer(arquivo_csv, delimiter=',')
    
    # Escrever o cabeçalho
    writer.writerow(["ID", "Player_name", "Manager_name", "Team", "Alias", "Status"])
    
    # Escrever os dados dos jogadores
    writer.writerows(jogadores_home)

print("Arquivo 'dados_jogadores_'"+abreviatura_home+"'.csv' criado com sucesso.")

#
#### TIME VISITANTE #####
#

# Lista de jogadores titulares
titulares_away = [
    22, "Everson",
    13, "Guilherme Arana",
    26, "Renzo Saravia",
    28, "Mauricio Lemos",
    34, "Jemerson",
    5, "Otavio",
    15, "Matias Zaracho",
    23, "Alan Franco",
    44, "Rubens",
    7, "Hulk",
    10, "Paulinho",
]

banco_away = [
    4, "Rever",
    8, "Edenilson",
    9, "Cristian Pavon",
    16, "Igor Rabello",
    17, "Igor Gomes",
    20, "Hyoran",
    27, "Paulo Vitor",
    31, "Matheus Mendes",
    38, "Pedrinho",
    42, "Carlos Eduardo",
    45, "Alisson Santana",
    49, "Patrick",
]

tecnico_away = "Luiz Felipe Scolari"
time_away = "Atletico Mineiro"
abreviatura_away = "CAM"

# Criar lista de jogadores com status (titular ou banco)
jogadores_away = []

for i in range(0, len(titulares_away), 2):
    jogador_id = titulares_away[i]
    jogador_nome = titulares_away[i + 1]
    jogadores_away.append([jogador_id, jogador_nome, tecnico_away, time_away, abreviatura_away, 1])

for i in range(0, len(banco_away), 2):
    jogador_id = banco_away[i]
    jogador_nome = banco_away[i + 1]
    jogadores_away.append([jogador_id, jogador_nome, tecnico_away, time_away, abreviatura_away, 2])

# Escrever os dados em um arquivo CSV
with open('Dados Jogadores/Dados_jogadores_'+abreviatura_away+'.csv', mode='w', newline='') as arquivo_csv:
    writer = csv.writer(arquivo_csv, delimiter=',')
    
    # Escrever o cabeçalho
    writer.writerow(["ID", "Player_name", "Manager_name", "Team", "Alias", "Status"])
    
    # Escrever os dados dos jogadores
    writer.writerows(jogadores_away)

print("Arquivo 'dados_jogadores_'"+abreviatura_away+"'.csv' criado com sucesso.")
