import tkinter as tk
from tkinter import ttk
import locale

def analisar_variacao(stocks):
    top_5_variacao = sorted(stocks, key=lambda x: x['change'], reverse=True)[:5]

    top5_window = tk.Toplevel()
    top5_window.title('Top 5 Variação')
    top5_window.geometry('800x200')

    frame_tabela_top5 = tk.Frame(top5_window)
    frame_tabela_top5.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 20))

    table_top5 = ttk.Treeview(frame_tabela_top5)
    table_top5['columns'] = ('Stock', 'Name', 'Close', 'Change', 'Market Cap', 'Sector')

    table_top5.column('#0', width=0, stretch='no')
    table_top5.column('Stock', anchor='center', width=80)
    table_top5.column('Name', anchor='w', width=200)
    table_top5.column('Close', anchor='center', width=100)
    table_top5.column('Change', anchor='center', width=100)
    table_top5.column('Market Cap', anchor='center', width=120)
    table_top5.column('Sector', anchor='w', width=200)

    table_top5.heading('#0', text='', anchor='w')
    table_top5.heading('Stock', text='Stock', anchor='center')
    table_top5.heading('Name', text='Name', anchor='w')
    table_top5.heading('Close', text='Close', anchor='center')
    table_top5.heading('Change', text='Change', anchor='center')
    table_top5.heading('Market Cap', text='Market Cap', anchor='center')
    table_top5.heading('Sector', text='Sector', anchor='w')

    table_top5.pack(fill=tk.BOTH, expand=True)

    for stock in top_5_variacao:
        if stock['market_cap'] is not None and stock['sector'] is not None:
            close_formatted = locale.currency(stock['close'], grouping=True)
            change = stock['change']
            change_formatted = f"{change:.2f}%"
            market_cap = stock['market_cap']
            market_cap_formatted = locale.currency(market_cap, grouping=True)
            sector = stock['sector']

            table_top5.insert('', 'end', text='',
                              values=(stock['stock'], stock['name'], close_formatted, change_formatted,
                                      market_cap_formatted, sector))
