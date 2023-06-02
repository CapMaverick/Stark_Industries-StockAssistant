# dados.py
import json
import shutil
import os
from datetime import datetime
from API import obter_dados

def salvar_historico():
    if not os.path.exists('Histórico'):
        os.makedirs('Histórico')

    shutil.copy('dados.json', os.path.join('Histórico', f'dados_{datetime.now().strftime("%Y%m%d%H%M%S")}.json'))

def atualizar_dados():
    dados = obter_dados()
    if dados:
        with open('dados.json', 'w') as file:
            json.dump(dados, file, indent=4)
        salvar_historico()
        return True
    else:
        return False
