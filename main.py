import tkinter as tk
from tkinter import ttk
import json
import locale

def exibir_dados():
    with open('dados.json', 'r') as file:
        dados = json.load(file)

    stocks = dados['stocks']

    # Configurar locale para o Brasil
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    root = tk.Tk()
    root.title('Dados das Ações')

    table = ttk.Treeview(root)
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

    for stock in stocks:
        close_formatted = locale.currency(stock['close'], grouping=True)
        change_formatted = f"{stock['change']:.2f}%"
        market_cap = stock['market_cap']
        market_cap_formatted = locale.currency(market_cap, grouping=True) if market_cap is not None else ''

        table.insert('', 'end', text='', values=(
            stock['stock'],
            stock['name'],
            close_formatted,
            change_formatted,
            market_cap_formatted,
            stock['sector']
        ))

    table.pack(expand=True, fill='both')

    root.mainloop()

exibir_dados()
