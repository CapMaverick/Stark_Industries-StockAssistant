import os
import json
import shutil
import tkinter as tk
from tkinter import messagebox

def comparar_dados(dados1, dados2):
    # Compara todos os dados dentro dos arquivos JSON
    return dados1 == dados2

def remover_arquivos_repetidos():
    # Verificar se a pasta "Histórico" existe
    if not os.path.exists('Histórico'):
        messagebox.showinfo('Remover Arquivos Repetidos', 'A pasta "Histórico" não existe.')
        return

    # Criar um dicionário para armazenar os dados dos arquivos
    dados_arquivos = {}

    # Percorrer todos os arquivos na pasta "Histórico"
    for file_name in os.listdir('Histórico'):
        file_path = os.path.join('Histórico', file_name)

        # Verificar se o arquivo é um arquivo JSON
        if os.path.isfile(file_path) and file_name.endswith('.json'):
            # Ler o arquivo JSON e obter os dados
            with open(file_path, 'r') as file:
                try:
                    dados = json.load(file)
                except json.JSONDecodeError:
                    messagebox.showwarning('Remover Arquivos Repetidos', f'Erro ao ler o arquivo JSON: {file_path}')
                    continue

            # Verificar se os dados já existem em algum arquivo anterior
            repetido = False
            for arquivo_anterior, dados_anteriores in dados_arquivos.items():
                if comparar_dados(dados, dados_anteriores):
                    repetido = True
                    break

            if repetido:
                os.remove(file_path)
            else:
                dados_arquivos[file_path] = dados

    quantidade_removidos = len(dados_arquivos)
    messagebox.showinfo('Remover Arquivos Repetidos', f'{quantidade_removidos} arquivo(s) repetido(s) removido(s).')

remover_arquivos_repetidos()
