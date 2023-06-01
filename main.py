import tkinter as tk
from tkinter import ttk
import json
import locale
import math

def exibir_dados():
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
            close_formatted = locale.currency(stock['close'], grouping=True)
            change_formatted = f"{stock['change']:.2f}%"
            market_cap = stock['market_cap']
            market_cap_formatted = locale.currency(market_cap, grouping=True) if market_cap is not None else ''

            table.insert('', 'end', text='',
                         values=(stock['stock'], stock['name'], close_formatted, change_formatted,
                                 market_cap_formatted, stock['sector']))

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
    frame_tabela.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 0))  # Adicionado pady=(20, 0) para espaço apenas na parte superior

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

    root.mainloop()

exibir_dados()
