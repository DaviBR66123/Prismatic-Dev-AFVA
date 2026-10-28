import re
from ui.utils import exibir_cabecalho, borda_topo, borda_linha, borda_baixo, gerar_hash_senha
from data.data_manager import carregar_dados, salvar_dados
import core.tarefas as core_tarefas
import core.ia_service as ia_service
import cronometro as cronometro
import Flashcards as Flashcards
from controllers.usuario_controller import criar_usuario_menu


def gerenciar_tarefas_menu(dados: dict, usuario: str, chave: str, titulo: str):
    while True:
        tarefas = dados[usuario][chave]

        if not tarefas:
            print("\nNenhuma tarefa cadastrada ainda.")
        else:
            print()
            for i, t in enumerate(tarefas, 1):
                status = "✅" if t["concluida"] else "⬜"
                print(f"{i}. [{status}] {t['titulo']}")
        print("\n" + "-"*30)
        print("1. Criar Tarefa | 2. Alternar Status | 3. Excluir Tarefa | 4. 🤖 Central de perguntas | 5. Voltar")
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            t_nome = input("Nome da tarefa: ").strip()
            if t_nome: core_tarefas.adicionar_tarefa(dados, usuario, chave, t_nome)
        elif opcao == "2":
            try:
                idx = int(input("Número da tarefa: ")) - 1
                core_tarefas.alternar_status_tarefa(dados, usuario, chave, idx)
                tarefa = dados[usuario][chave][idx]
                if tarefa["concluida"]:
                    input(f"\n✅ Tarefa '{tarefa['titulo']}' marcada como concluída! Pressione Enter.")
                else:
                    input(f"\n↩️ Tarefa '{tarefa['titulo']}' marcada como pendente. Pressione Enter.")
            except (ValueError, IndexError):
                input("\nNúmero inválido. Pressione Enter.")
        elif opcao == "3":
            try:
                idx = int(input("Número da tarefa a excluir: ")) - 1
                tarefa = dados[usuario][chave][idx]
                confirmar = input(f"Tem certeza que quer excluir '{tarefa['titulo']}'? (s/n): ").lower()
                if confirmar == "s":
                    core_tarefas.excluir_tarefa(dados, usuario, chave, idx)
                    input("\n🗑️ Tarefa excluída. Pressione Enter.")
                else:
                    input("\nExclusão cancelada. Pressione Enter.")
            except (ValueError, IndexError):
                input("\nNúmero inválido. Pressione Enter.")
        elif opcao == "4":
            try:
                idx = int(input("Número da tarefa para IA tratar: ")) - 1
                tarefas = dados[usuario][chave]
                if 0 <= idx < len(tarefas):
                    passos = ia_service.gerar_passos_tarefa(tarefas[idx]["titulo"])
                    print("\n🤖 Passos sugeridos pela IA:")
                    for i, p in enumerate(passos, 1): print(f"  {i}. {p}")
                    if input("\nAceitar sugestão? (s/n): ").lower() == 's':
                        core_tarefas.injetar_passos_ia(dados, usuario, chave, idx, passos)
            except ValueError: pass
        elif opcao == "5":
            break


def menu_metodos_estudo():
    while True:
        exibir_cabecalho("MÉTODOS DE ESTUDO")
        print("1. Cronômetro Pomodoro")
        print("2. Flashcards")
        print("3. Voltar")
        opcao = input("\nEscolha: ").strip()
        if opcao == "1":
            cronometro.pomodoro_timer()
        elif opcao == "2":
            caminho = Flashcards.selecionar_pdf()
            if caminho:
                texto = Flashcards.extrair_texto_pdf(caminho)
                flashcards = Flashcards.criar_flashcards(texto)
                if flashcards:
                    Flashcards.estudar_flashcards(flashcards)
                else:
                    input("\nNenhum flashcard criado. Pressione Enter.")
            else:
                input("\nNenhum arquivo selecionado. Pressione Enter.")
        elif opcao == "3":
            break

def painel_ia_menu(dados: dict, usuario: str):
    exibir_cabecalho("ASSISTENTE DE IA")
    print("Peça ajuda para simplificar enunciados, organizar rotinas ou tirar dúvidas.")
    estilo = dados[usuario]["preferencias"]["estilo_instrucao"]

    while True:
        pergunta = input("\nPergunta (ou 'sair'): ").strip()
        if pergunta.lower() == 'sair':
            break
        if not pergunta:
            continue

        print("\n🤖 Processando...")
        respostas = ia_service.obter_resposta_ia(pergunta, estilo)
        print(f"\n[Assistente - Modo {estilo.upper()}]:")
        for linha in respostas:
            print(f"- {linha}")
        print("-" * 30)

        print("\n1. Fazer outra pergunta")
        print("2. Voltar ao menu principal")
        opcao_pos = ""
        while opcao_pos not in ("1", "2"):
            opcao_pos = input("Escolha uma opção: ").strip()
        if opcao_pos == "2":
            break

def painel_principal_menu(dados: dict, usuario: str):
    while True:
        exibir_cabecalho(f"PAINEL DO USUÁRIO: {usuario}")
        print("1. Atividades Diárias")
        print("2. Estudos e Atividades")
        print("3. 🤖 Central de IA")
        print("4. Métodos de estudo")
        print("5. Logout")
        opcao = input("\nEscolha: ").strip()
        if opcao == "1":
            gerenciar_tarefas_menu(dados, usuario, "tarefas_diarias", "ROTINA DIÁRIA")
        elif opcao == "2":
            gerenciar_tarefas_menu(dados, usuario, "tarefas_educacionais", "ESTUDOS E EDUCAÇÃO")
        elif opcao == "3":
            painel_ia_menu(dados, usuario)
        elif opcao == "4":
            menu_metodos_estudo()
        elif opcao == "5":
            break