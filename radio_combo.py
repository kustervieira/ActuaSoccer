import tkinter as tk
from tkinter import ttk
import csv

def on_radio_button_selected(event):
    selected_value = radio_var.get()
    combo['values'] = [100] if selected_value == 1 else [200]
    combo.set('')  # Limpa a seleção atual, se houver

def display_selected_value(event):
    value = combo.get()
    if value:
        tree.insert("", "end", values=(value,))

def save_to_csv():
    value = combo.get()
    if value:
        selected_values.append(value)
        combo.set('')  # Limpa a seleção atual
        with open('dados.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Valor"])
            for val in selected_values:
                writer.writerow([val])

# Cria uma janela
root = tk.Tk()
root.title("Exemplo Tkinter")

# Variável para armazenar a seleção do RadioButton
radio_var = tk.IntVar()

# Lista para armazenar os valores selecionados
selected_values = []

# Cria os RadioButtons
radio_button1 = tk.Radiobutton(root, text="Opção 1", variable=radio_var, value=1)
radio_button1.pack()

radio_button2 = tk.Radiobutton(root, text="Opção 2", variable=radio_var, value=2)
radio_button2.pack()

# Cria um ComboBox inicialmente vazio
combo = ttk.Combobox(root, values=[], state="readonly")
combo.pack()

# Botão para salvar o valor selecionado
save_button = tk.Button(root, text="Salvar", command=save_to_csv)
save_button.pack()

# Cria uma TreeView para exibir os valores selecionados
tree = ttk.Treeview(root, columns=("Valor",), show="headings")
tree.heading("Valor", text="Valor")
tree.pack()

# Associa o evento de seleção do RadioButton à função
radio_button1.bind('<Button-1>', on_radio_button_selected)
radio_button2.bind('<Button-1>', on_radio_button_selected)

# Associa o evento de seleção do ComboBox à função de exibição
combo.bind("<<ComboboxSelected>>", display_selected_value)

# Inicia o loop principal
root.mainloop()
