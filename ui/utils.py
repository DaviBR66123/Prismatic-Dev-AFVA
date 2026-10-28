import os
import re
import hashlib

def gerar_hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_cabecalho(titulo: str):
    limpar_tela()
    borda_topo()
    print("|" + titulo.center(LARGURA - 2) + "|")
    borda_baixo()
    print()
LARGURA = 60

def borda_topo():
    print("+" + "-" * (LARGURA - 2) + "+")

def borda_linha(texto: str = ""):
    print("|" + texto.ljust(LARGURA - 2) + "|")

def borda_baixo():
    print("+" + "-" * (LARGURA - 2) + "+")

def validar_email(email: str) -> bool:
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None