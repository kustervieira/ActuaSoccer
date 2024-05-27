import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Exemplo Tkinter")

selected_values = []

combo1 = ttk.Combobox(root, values=["1", "2"], state="readonly")
combo1.pack()

values_combo2 = ttk.Combobox(root, values=[], state="readonly")
values_combo2.pack()

values_combo3 = ttk.Combobox(root, values=[], state="readonly")
values_combo3.pack()

tree = ttk.Treeview(root, columns=("Values",), show="headings")
tree.heading("Values", text="Values")
tree.pack()

def on_combo1_selected(event):
    selected_value = combo1.get()
    if selected_value == "1":
        values_combo2['values'] = ["100"]
        values_combo3['values'] = ["Cem", "oi", "OLA"]
    elif selected_value == "2":
        values_combo2['values'] = ["4", "5", "6"]
        values_combo3['values'] = ["Palmares", "SEM"]
    else:
        values_combo2['values'] = []
        values_combo3['values'] = []

    update_tree()

def on_combo2_selected(event):
    selected_value = values_combo2.get()
    if selected_value == "6":
        values_combo3['values'] = ["Mundial"]
    else:
        values_combo3['values'] = []
    update_tree()

def on_combo3_selected(event):
    update_tree()

def update_tree():
    for item in tree.get_children():
        tree.delete(item)
    value2 = values_combo2.get()
    value3 = values_combo3.get()
    if value2:
        tree.insert("", "end", values=(value2,))
    if value3:
        tree.insert("", "end", values=(value3,))

combo1.bind("<<ComboboxSelected>>", on_combo1_selected)
values_combo2.bind("<<ComboboxSelected>>", on_combo2_selected)
values_combo3.bind("<<ComboboxSelected>>", on_combo3_selected)

root.mainloop()
