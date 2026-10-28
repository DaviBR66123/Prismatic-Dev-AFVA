from data.data_manager import carregar_dados
from ui.menus import criar_usuario_menu, painel_principal_menu
from ui.utils import exibir_cabecalho, gerar_hash_senha

def executar_sistema():
    while True:
        dados = carregar_dados()
        exibir_cabecalho("SISTEMA A.F.V.A")
        print("1. Entrar com um perfil de estudante")
        print("2. Criar novo perfil de estudante")
        print("3. Encerrar")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            if not dados:
                input("\nNenhum perfil salvo. Crie um primeiro! (Enter)")
                continue

            email = input("\nEmail: ").strip().lower()
            senha = input("Senha: ").strip()
            senha_hash = gerar_hash_senha(senha)

            nome_encontrado = None
            for nome, info in dados.items():
                if info.get("email") == email and info.get("senha") == senha_hash:
                    nome_encontrado = nome
                    break

            if nome_encontrado:
                painel_principal_menu(dados, nome_encontrado)
            else:
                input("\nEmail ou senha incorretos! (Enter)")
        elif opcao == "2":
            criar_usuario_menu(dados)
        elif opcao == "3":
            print("\nAté logo estudante!")
            break

if __name__ == "__main__":
    executar_sistema()