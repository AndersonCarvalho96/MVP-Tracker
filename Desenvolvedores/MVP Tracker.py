import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime, timedelta
import csv
import ctypes
import sys
from tkinter import Tk, messagebox


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def require_admin():
    if not is_admin():
        # Mostrar uma mensagem de erro se não estiver como administrador
        root = Tk()
        root.withdraw()  # Ocultar a janela principal
        messagebox.showerror(
            "Erro", "Este aplicativo deve ser executado como administrador.")
        sys.exit(1)  # Encerrar o aplicativo


# Verificar se o script está sendo executado como administrador
require_admin()


# Conectando ao banco de dados SQLite
conn = sqlite3.connect('mvp_tracker.db')
cursor = conn.cursor()

# Criando a tabela se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS mvps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mvp TEXT NOT NULL,
    mapa TEXT NOT NULL,
    tempo_respawn INTEGER NOT NULL,
    hora_morte TEXT,
    coordenadas TEXT,
    nasce_as TEXT
)
''')
conn.commit()

# Função para calcular "Nasce as"


def calcular_nasce_as(hora_morte, tempo_respawn):
    hora_morte_dt = datetime.strptime(hora_morte, '%H:%M')
    nasce_as_dt = hora_morte_dt + timedelta(minutes=tempo_respawn)
    return nasce_as_dt.strftime('%H:%M')

# Função para adicionar um novo MVP


def adicionar_mvp():
    mvp = entry_mvp.get()
    mapa = entry_mapa.get()
    tempo_respawn = int(entry_tempo_respawn.get())
    hora_morte = entry_hora_morte.get()
    coordenadas = entry_coordenadas.get()

    nasce_as = calcular_nasce_as(hora_morte, tempo_respawn)

    cursor.execute('''
    INSERT INTO mvps (mvp, mapa, tempo_respawn, hora_morte, coordenadas, nasce_as)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (mvp, mapa, tempo_respawn, hora_morte, coordenadas, nasce_as))
    conn.commit()
    carregar_dados()

# Função para editar um MVP existente


def editar_mvp():
    selected_item = tree.selection()[0]
    mvp = entry_mvp.get()
    mapa = entry_mapa.get()
    tempo_respawn = int(entry_tempo_respawn.get())
    hora_morte = entry_hora_morte.get()
    coordenadas = entry_coordenadas.get()

    nasce_as = calcular_nasce_as(hora_morte, tempo_respawn)

    cursor.execute('''
    UPDATE mvps SET mapa = ?, tempo_respawn = ?, hora_morte = ?, coordenadas = ?, nasce_as = ?
    WHERE id = ?
    ''', (mapa, tempo_respawn, hora_morte, coordenadas, nasce_as, tree.item(selected_item)['values'][0]))
    conn.commit()
    carregar_dados()

# Função para excluir um MVP


def excluir_mvp():
    selected_item = tree.selection()
    if selected_item:
        # Ajustado para o índice correto
        item_id = tree.item(selected_item[0])['values'][0]

        cursor.execute('DELETE FROM mvps WHERE id = ?', (item_id,))
        conn.commit()
        carregar_dados()
    else:
        print("Nenhum item selecionado.")


# Função para carregar os dados na Treeview


def carregar_dados():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute('SELECT * FROM mvps')
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

# Função para ordenar as colunas


def ordenar_coluna(coluna, reverse=False):
    dados = [(tree.set(k, coluna), k) for k in tree.get_children('')]
    if coluna in ['tempo_respawn', 'nasce_as', 'hora_morte']:
        dados.sort(key=lambda t: int(t[0].replace(
            ':', '')) if ':' in t[0] else int(t[0]), reverse=reverse)
    else:
        dados.sort(reverse=reverse)

    for index, (val, k) in enumerate(dados):
        tree.move(k, '', index)

    tree.heading(coluna, command=lambda: ordenar_coluna(coluna, not reverse))

# Função para selecionar um MVP na Treeview


def selecionar_mvp(event):
    selected_item = tree.selection()
    if selected_item:
        valores = tree.item(selected_item[0])['values']

        entry_mvp.delete(0, tk.END)
        entry_mvp.insert(tk.END, valores[1])

        entry_mapa.delete(0, tk.END)
        entry_mapa.insert(tk.END, valores[2])

        entry_tempo_respawn.delete(0, tk.END)
        entry_tempo_respawn.insert(tk.END, valores[3])

        entry_hora_morte.delete(0, tk.END)
        entry_hora_morte.insert(tk.END, valores[4])

        entry_coordenadas.delete(0, tk.END)
        entry_coordenadas.insert(tk.END, valores[5])


# Função para exportar os dados para um arquivo CSV


def exportar_dados():
    arquivo = filedialog.asksaveasfilename(
        defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if arquivo:
        with open(arquivo, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            cursor.execute('SELECT * FROM mvps')
            writer.writerow([i[0] for i in cursor.description])
            for row in cursor.fetchall():
                writer.writerow(row)

# Função para importar dados de um arquivo CSV


def importar_dados():
    arquivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if arquivo:
        with open(arquivo, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute('''
                INSERT INTO mvps (mvp, mapa, tempo_respawn, hora_morte, coordenadas, nasce_as)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (row['mvp'], row['mapa'], row['tempo_respawn'], row['hora_morte'], row['coordenadas'], row['nasce_as']))
            conn.commit()
        carregar_dados()


# Criando a interface gráfica com tkinter
root = tk.Tk()
root.title("MVP Tracker")
root.geometry("770x500")
root.resizable(False, False)

# Carregar a imagem de fundo
background_image = Image.open("background-MVP.jpg")
background_image = background_image.resize(
    (870, 500))

# Adicionar transparência à imagem
alpha = Image.new('L', background_image.size, int(255 * 0.6))  # 60% opacidade
background_image.putalpha(alpha)

background_photo = ImageTk.PhotoImage(background_image)

# Adicionar a imagem de fundo
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Criando os campos de entrada
font_style = ('Arial', 10, 'bold')
label_bg_color = '#FFB347'

tk.Label(root, text="MVP:", font=font_style, bg=label_bg_color, anchor='w', relief='solid', bd=2).grid(
    row=0, column=0, padx=5, pady=5, sticky='w')
entry_mvp = tk.Entry(root, font=font_style, bg='white')
entry_mvp.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Mapa:", font=font_style, bg=label_bg_color, anchor='w', relief='solid', bd=2).grid(
    row=1, column=0, padx=5, pady=5, sticky='w')
entry_mapa = tk.Entry(root, font=font_style, bg='white')
entry_mapa.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Tempo de Respawn (min):", font=font_style, bg=label_bg_color,
         anchor='w', relief='solid', bd=2).grid(row=2, column=0, padx=5, pady=5, sticky='w')
entry_tempo_respawn = tk.Entry(root, font=font_style, bg='white')
entry_tempo_respawn.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Hora da Morte (HH:MM):", font=font_style, bg=label_bg_color,
         anchor='w', relief='solid', bd=2).grid(row=3, column=0, padx=5, pady=5, sticky='w')
entry_hora_morte = tk.Entry(root, font=font_style, bg='white')
entry_hora_morte.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Coordenadas:", font=font_style, bg=label_bg_color,
         anchor='w', relief='solid', bd=2).grid(row=4, column=0, padx=5, pady=5, sticky='w')
entry_coordenadas = tk.Entry(root, font=font_style, bg='white')
entry_coordenadas.grid(row=4, column=1, padx=5, pady=5)

# Botões de ação
btn_adicionar = tk.Button(root, text="Adicionar",
                          command=adicionar_mvp, bg='black', fg='white')
btn_adicionar.grid(row=5, column=0, padx=5, pady=5)

btn_editar = tk.Button(root, text="Editar",
                       command=editar_mvp, bg='black', fg='white')
btn_editar.grid(row=5, column=1, padx=5, pady=5)

btn_excluir = tk.Button(root, text="Excluir",
                        command=excluir_mvp, bg='black', fg='white')
btn_excluir.grid(row=5, column=2, padx=5, pady=5)

# Criando a Treeview para exibir os dados
tree = ttk.Treeview(root, columns=(
    'id', 'mvp', 'mapa', 'tempo_respawn', 'hora_morte', 'coordenadas', 'nasce_as'), show='headings')

# Definindo o cabeçalho das colunas
tree.heading('id', text='ID', command=lambda: ordenar_coluna('id'))
tree.heading('mvp', text='MVP', command=lambda: ordenar_coluna('mvp'))
tree.heading('mapa', text='Mapa', command=lambda: ordenar_coluna('mapa'))
tree.heading('tempo_respawn', text='Tempo Respawn (min)',
             command=lambda: ordenar_coluna('tempo_respawn'))
tree.heading('hora_morte', text='Hora da Morte',
             command=lambda: ordenar_coluna('hora_morte'))
tree.heading('coordenadas', text='Coordenadas',
             command=lambda: ordenar_coluna('coordenadas'))
tree.heading('nasce_as', text='Nasce às',
             command=lambda: ordenar_coluna('nasce_as'))

# Ocultando a coluna ID
tree.column('id', width=0, stretch=tk.NO)

# Definindo o estilo para as colunas
tree.column('mvp', width=120, anchor='center')
tree.column('mapa', width=120, anchor='center')
tree.column('tempo_respawn', width=150, anchor='center')
tree.column('hora_morte', width=120, anchor='center')
tree.column('coordenadas', width=120, anchor='center')
tree.column('nasce_as', width=120, anchor='center')

# Aplicando o estilo de fonte em negrito para os cabeçalhos
style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))

# Posicionando a Treeview na interface
tree.grid(row=6, column=0, columnspan=3, padx=5, pady=5)


# Conectando a seleção de itens na Treeview à função selecionar_mvp
tree.bind('<<TreeviewSelect>>', selecionar_mvp)

# Botões de importação e exportação
btn_importar = tk.Button(root, text="Importar",
                         command=importar_dados, bg='black', fg='white')
btn_importar.grid(row=7, column=0, padx=5, pady=5)

btn_exportar = tk.Button(root, text="Exportar",
                         command=exportar_dados, bg='black', fg='white')
btn_exportar.grid(row=7, column=1, padx=5, pady=5)

# Carregando os dados iniciais na Treeview
carregar_dados()

# Iniciando o loop principal da interface gráfica
root.mainloop()

# Fechando a conexão com o banco de dados ao encerrar o aplicativo
conn.close()
