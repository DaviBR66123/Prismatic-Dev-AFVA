import os
from typing import Dict, Any

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def conectar():
    """
    Abre uma conexão com o banco MySQL.

    Antes de executar o sistema, confira o arquivo .env:
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=sua_senha
    DB_NAME=tpac_db
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "tpac_db"),
        port=int(os.getenv("DB_PORT", "3306"))
    )


def carregar_dados() -> Dict[str, Any]:
    """
    Busca os usuários, tarefas e passos no MySQL e monta a mesma estrutura
    que antes era lida do arquivo tpac_users.json.
    """
    dados = {}

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, nome, email, senha, estilo_instrucao
        FROM usuarios
        ORDER BY nome
    """)
    usuarios = cursor.fetchall()

    for usuario in usuarios:
        nome = usuario["nome"]

        dados[nome] = {
            "email": usuario["email"],
            "senha": usuario["senha"],
            "preferencias": {
                "estilo_instrucao": usuario["estilo_instrucao"]
            },
            "tarefas_diarias": [],
            "tarefas_educacionais": []
        }

        cursor.execute("""
            SELECT id, titulo, concluida, tipo
            FROM tarefas
            WHERE usuario_id = %s
            ORDER BY id
        """, (usuario["id"],))
        tarefas = cursor.fetchall()

        for tarefa in tarefas:
            tarefa_dict = {
                "titulo": tarefa["titulo"],
                "concluida": bool(tarefa["concluida"]),
                "passos": []
            }

            cursor.execute("""
                SELECT texto, concluido
                FROM passos
                WHERE tarefa_id = %s
                ORDER BY ordem
            """, (tarefa["id"],))
            passos = cursor.fetchall()

            for passo in passos:
                tarefa_dict["passos"].append({
                    "texto": passo["texto"],
                    "concluido": bool(passo["concluido"])
                })

            dados[nome][tarefa["tipo"]].append(tarefa_dict)

    cursor.close()
    conexao.close()

    return dados


def salvar_dados(dados: Dict[str, Any]) -> None:
    """
    Salva no MySQL as tarefas e os passos.

    A tabela usuarios NÃO é mais apagada nem reconstruída aqui — ela já é
    gerenciada pelo UsuarioRepository (usado pela API e pelo menu de criar
    perfil). Esta função só cuida de tarefas e passos, buscando o id do
    usuário já existente pelo nome.
    """
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("TRUNCATE TABLE passos")
        cursor.execute("TRUNCATE TABLE tarefas")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        for nome, info_usuario in dados.items():
            cursor.execute("SELECT id FROM usuarios WHERE nome = %s", (nome,))
            linha = cursor.fetchone()

            if linha is None:
                continue

            usuario_id = linha[0]

            for tipo in ["tarefas_diarias", "tarefas_educacionais"]:
                for tarefa in info_usuario.get(tipo, []):
                    cursor.execute("""
                        INSERT INTO tarefas (usuario_id, tipo, titulo, concluida)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        usuario_id,
                        tipo,
                        tarefa.get("titulo", ""),
                        bool(tarefa.get("concluida", False))
                    ))

                    tarefa_id = cursor.lastrowid

                    for ordem, passo in enumerate(tarefa.get("passos", []), start=1):
                        cursor.execute("""
                            INSERT INTO passos (tarefa_id, texto, concluido, ordem)
                            VALUES (%s, %s, %s, %s)
                        """, (
                            tarefa_id,
                            passo.get("texto", ""),
                            bool(passo.get("concluido", False)),
                            ordem
                        ))

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise

    finally:
        cursor.close()
        conexao.close()