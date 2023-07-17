import re
import time

from commands import Receive_Cmd, Send_Cmd
from rich import print

from util import split_string


def check_terminal_alive(client):
    # comando = "#live?"
    print('Check online status')
    comando = Send_Cmd.ALIVE.value.encode('ascii')
    client.send(comando)
    time.sleep(0.5)
    resposta = client.recv(255)
    resposta = resposta.decode('ascii')
    # print(resposta + '\n')
    print('OK')
    return


def set_always_on(client):
    resposta = None  # Variável para guardar a resposta
    print('Set always mode')
    comando = Send_Cmd.ALWAYS_ON.value  # Transforma a string em bytes
    client.send(comando)  # Envia o comando para o equipamento
    time.sleep(0.5)  # Tempo para garantir resposta do equipamento
    dados = client.recv(255)  # Faz a leitura da resposta do Busca Preço
    resposta = dados.decode('ascii')  # Converte os bytes para texto.
    if Receive_Cmd.RESPONSE_ALWAYS_ON.value in resposta:
        print('OK')
    else:
        print(f'Retorno inválido {resposta}')


def await_terminal_query(client):
    while True:
        print('Awaiting for query')
        # dados = client.recv(255).decode('ascii')
        dados = client.recv(255).decode("utf8")
        # time.sleep(0.5)
        print(f'Consultando: {dados}')
        if terminal_input_valid(dados):
            return_query(client)
        else:
            print('Invalid terminal return')


def return_query(client):
    # Define os parâmetros que serão enviados na função
    Linha1 = "TIJOLO 6 FUROS PARA REFORMA DE CASAS PARA"[:40] \
        + " " + "125,35"
    Linha1 = split_string(Linha1, 20, True)
    str = Linha1 
    comando = str.encode("cp1255")  # Transforma a string em bytes
    client.send(comando)  # Envia o comando para o equipamento
    print(f'Resposta consulta retornada: {str}')
    # time.sleep(5)
    return

def terminal_input_valid(string):
    pattern = r'^#(\d)'
    match = re.match(pattern, string)
    if match:
        return True
    return False