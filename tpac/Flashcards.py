import random
import PyPDF2
import tkinter as tk
from tkinter import filedialog

def selecionar_pdf():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    caminho = filedialog.askopenfilename(
        title="Selecione um arquvo PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )

    return caminho

def extrair_texto_pdf(caminho_pdf):
    texto = ""

    with open(caminho_pdf, "rb") as arquivo:
        leitor = PyPDF2.PdfReader(arquivo)

        for pagina in leitor.pages:
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto += texto_pagina + "\n"

    return texto

def criar_flashcards(texto):
    frases = [f.strip() for f in texto.split("\n") if len(f.strip()) > 20]

    flashcards = []

    for frase in frases:
        palavras = frase.split()

        if len(palavras) > 5:
            pergunta = "Complete a frase:\n\n" + " ".join(palavras[:5]) + " ..."
        else:
            pergunta = "Complete a frase."

        resposta = frase
        flashcards.append((pergunta, resposta))

    return flashcards

def estudar_flashcards(flashcards):
    print("Modo Flashcards iniciado!")

    while True:
        pergunta, resposta = random.choice(flashcards)

        print("\n" + "=" * 50)
        print("Pergunta:")
        print(pergunta)

        input("\nPressione ENTER para ver a resposta...")

        print("\nResposta:")
        print(resposta)

        continuar = input("\nQuer continuar? (s/n): ").lower()

        if continuar != "s":
            print("\nSessão encerrada. Você foi muito bem!")
            break

if __name__ == "__main__":
    caminho = selecionar_pdf()

    if not caminho:
        print("Nenhum arquivo foi selecionado.")
        exit()

    try:
        texto = extrair_texto_pdf(caminho)

        if not texto.strip():
            print("Não foi possível extrair texto do PDF.")
            exit()

        flashcards = criar_flashcards(texto)

        if not flashcards:
            print("Nenhum flashcard pode ser criado.")
            exit()

        estudar_flashcards(flashcards)

    except Exception as erro:
        print(f"Erro: {erro}")
        