import tkinter as tk
from tkinter import ttk
import json
import locale
import math
import shutil
import os
from datetime import datetime
import requests
from tkinter import messagebox

def obter_dados():
    response = requests.get('https://brapi.dev/api/quote/list')
    if response.status_code == 200:
        return response.json()
    else:
        print('Falha ao obter dados da API')
        return None

def salvar_historico():
    # Verificar se a pasta "Histórico" existe, caso contrário, criar a pasta
    if not os.path.exists('Histórico'):
        os.makedirs('Histórico')

    # Fazer uma cópia do arquivo de dados.json na pasta "Histórico" com um nome único
    shutil.copy('dados.json', os.path.join('Histórico', f'dados_{datetime.now().strftime("%Y%m%d%H%M%S")}.json'))

def atualizar_dados():
    dados = obter_dados()
    if dados:
        with open('dados.json', 'w') as file:
            json.dump(dados, file, indent=4)
        salvar_historico()  # Adicionado para salvar o histórico
        return True
    else:
        return False

def exibir_dados():
    # Verificar se o arquivo de dados.json existe, caso contrário, realizar a primeira atualização dos dados
    if not os.path.exists('dados.json'):
        if not atualizar_dados():
            return

    with open('dados.json', 'r') as file:
        dados = json.load(file)

    stocks = dados['stocks']

    # Configurar locale para o Brasil
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    # Função para atualizar a tabela com os dados da página atual
    def atualizar_tabela():
        nonlocal lbl_pagina_atual  # Adicionado para tornar a variável acessível
        table.delete(*table.get_children())
        for stock in stocks[current_page * items_per_page: (current_page + 1) * items_per_page]:
            if stock['market_cap'] is not None and stock['sector'] is not None:
                close_formatted = locale.currency(stock['close'], grouping=True)
                change = stock['change']
                change_formatted = f"{change:.2f}%"
                market_cap = stock['market_cap']
                market_cap_formatted = locale.currency(market_cap, grouping=True)
                sector = stock['sector']

                table.insert('', 'end', text='',
                             values=(stock['stock'], stock['name'], close_formatted, change_formatted,
                                     market_cap_formatted, sector))

        lbl_pagina_atual.config(text=f"Página: {current_page + 1}/{total_pages}")

    # Função para ir para a página anterior
    def pagina_anterior():
        nonlocal current_page
        if current_page > 0:
            current_page -= 1
            atualizar_tabela()

    # Função para ir para a próxima página
    def proxima_pagina():
        nonlocal current_page
        if (current_page + 1) * items_per_page < len(stocks):
            current_page += 1
            atualizar_tabela()

    root = tk.Tk()
    root.title('Dados das Ações')
    root.geometry('800x600')  # Definir tamanho fixo da janela

    frame_tabela = tk.Frame(root)
    frame_tabela.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 0))

    table = ttk.Treeview(frame_tabela)
    table['columns'] = ('Stock', 'Name', 'Close', 'Change', 'Market Cap', 'Sector')

    table.column('#0', width=0, stretch='no')
    table.column('Stock', anchor='center', width=80)
    table.column('Name', anchor='w', width=200)
    table.column('Close', anchor='center', width=100)
    table.column('Change', anchor='center', width=100)
    table.column('Market Cap', anchor='center', width=120)
    table.column('Sector', anchor='w', width=200)

    table.heading('#0', text='', anchor='w')
    table.heading('Stock', text='Stock', anchor='center')
    table.heading('Name', text='Name', anchor='w')
    table.heading('Close', text='Close', anchor='center')
    table.heading('Change', text='Change', anchor='center')
    table.heading('Market Cap', text='Market Cap', anchor='center')
    table.heading('Sector', text='Sector', anchor='w')

    table.pack(fill=tk.BOTH, expand=True)

    # Paginação
    items_per_page = 50
    current_page = 0
    total_pages = math.ceil(len(stocks) / items_per_page)

    lbl_pagina_atual = tk.Label(root, text=f"Página: {current_page + 1}/{total_pages}")
    lbl_pagina_atual.pack(pady=10)

    frame_botoes = tk.Frame(root)
    frame_botoes.pack()

    btn_anterior = tk.Button(frame_botoes, text='Anterior', command=pagina_anterior)
    btn_anterior.pack(side=tk.LEFT)

    btn_proxima = tk.Button(frame_botoes, text='Próxima', command=proxima_pagina)
    btn_proxima.pack(side=tk.LEFT)

    atualizar_tabela()

    # Verificar se houve atualização dos dados e mostrar mensagem de confirmação
    if atualizar_dados():
        messagebox.showinfo('Atualização', 'Os dados foram atualizados com sucesso e o arquivo antigo foi salvo no histórico.')
    else:
        messagebox.showerror('Atualização', 'Falha ao atualizar os dados.')

    root.mainloop()

exibir_dados()
