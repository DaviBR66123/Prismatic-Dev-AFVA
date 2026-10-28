import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None
MODELO_GEMINI = "gemini-2.5-flash"


def _obter_instrucao_por_estilo(estilo_usuario: str) -> str:
    base_prompt = (
        "Você é um assistente especializado em acessibilidade para pessoas com TPAC, TDAH, DEA ou depressão.\n"
        "Seu papel é reduzir a carga cognitiva, cansaço mental e ambiguidade.\n"
        "Diretrizes obrigatórias:\n"
        "- prefira não usar, apenas se necessário use parágrafos longos, blocos densos de texto ou jargões complexos.\n"
        "- Use frases curtas, ordem direta (Sujeito + Verbo + Objeto).\n"
        "- Divida as respostas visualmente usando tópicos/bullets claros.\n"
        "lembre das últimas perguntas do usuário caso ele queira fazer perguntas relacionados.\n"
    )
    extras = {
    "direto":    "- Seja objetivo e conciso. use poucas linhas de texto mas sem perder o essencial da explicação.",
    "detalhado": "- Explique passo a passo, de forma lógica e sequencial. "
                 "Primeiro contextualize o problema, depois detalhe cada etapa "
                 "com o raciocínio por trás dela, e finalize com um resumo "
                 "do que foi feito e por quê.",
    "tdah":      "- Frases curtas. Uma ação por linha. Direto ao ponto. "
                 "Nada de texto longo.",
    "tea":       "- Seja literal e específico, evite metáforas, ironias ou linguagem "
                 "figurada. Use frases claras e objetivas, sempre na mesma estrutura. "
                 "Explique passo a passo, sem ambiguidade. Evite sobrecarga de "
                 "informação: um assunto por vez.",
    "depressao": "- Vá com calma. Sem pressa, sem cobrança. Cada passo que "
                 "a pessoa der já é suficiente. Reconheça o esforço dela, "
                 "acolha onde ela estiver, e nunca insinue que deveria "
                 "estar fazendo mais.",
}
    base_prompt += extras.get(estilo_usuario, extras["direto"])
    return base_prompt

def obter_resposta_ia(pergunta: str, estilo_usuario: str) -> list:
    if not client:
        return [
            "Erro: GEMINI_API_KEY não encontrada no arquivo .env.",
            "Abra o arquivo .env e preencha: GEMINI_API_KEY=sua_chave_aqui"
        ]
    system_instruction = _obter_instrucao_por_estilo(estilo_usuario)

    tentativas = 3
    for tentativa in range(tentativas):
        try:
            response = client.models.generate_content(
                model=MODELO_GEMINI,
                contents=pergunta,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.3,
                ),
            )
            return [linha.strip() for linha in response.text.split("\n") if linha.strip()]

        except Exception as e:
            if "503" in str(e) and tentativa < tentativas - 1:
                print(f"\n⚠️ Serviço ocupado. Tentando novamente ({tentativa + 1}/{tentativas})...")
                time.sleep(3)
            else:
                return [f"Erro ao se comunicar com a IA: {str(e)}"]


def gerar_passos_tarefa(titulo_tarefa: str) -> list:
    if not client:
        return [
            "Erro: GEMINI_API_KEY não encontrada no arquivo .env.",
            "Abra o arquivo .env e preencha: GEMINI_API_KEY=sua_chave_aqui"
        ]
    prompt = (
        f"Quebre a seguinte tarefa entre 3 a 10 passos sequenciais, "
        f"curtos e fáceis de focar: '{titulo_tarefa}'. "
        f"Escreva apenas os passos, um por linha, se quiser use introduções ou numeração manual."
        f"lembre da resposta anterior do terminal para responder caso a pessoa queira resumir ou que explique mais detalhadamente"
    )
    system_instruction = (
        "Você é um especialista em produtividade para neurodivergentes. "
        "Crie checklists limpos, com verbos de ação claros e livres de poluição textual."
    )
    tentativas = 3
    for tentativa in range(tentativas):
        try:
            response = client.models.generate_content(
                model=MODELO_GEMINI,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.2,
                ),
            )
            passos = [linha.strip() for linha in response.text.split("\n") if linha.strip()]
            passos_limpos = []
            for p in passos:
                p_limpo = p.lstrip("0123456789.-* ")
                if p_limpo:
                    passos_limpos.append(p_limpo)
            return passos_limpos

        except Exception as e:
            if "503" in str(e) and tentativa < tentativas - 1:
                print(f"\n⚠️ Serviço ocupado. Tentando novamente ({tentativa + 1}/{tentativas})...")
                time.sleep(3)
            else:
                return [f"Não foi possível gerar os passos: {str(e)}"]