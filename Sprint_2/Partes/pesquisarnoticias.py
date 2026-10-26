import dspy
import requests
from newsapi import NewsApiClient

# Insira aqui o Token do seu bot (obtido com o @BotFather)
TOKEN = "Seu_Token"
# Insira aqui o ID do chat ou canal
CHAT_ID = "Seu_ID"
# Inicialize o cliente com a sua chave de API
newsapi = NewsApiClient(api_key="Seu_NewsAPI_Key")

# LLM local (se este código for parar dentro do arquivo do bot, remova estas 2 linhas)
lm = dspy.LM("ollama_chat/qwen2.5-coder:7b", api_base="http://localhost:11434", api_key="")
dspy.configure(lm=lm)


# ----------------------------------------------------------------------
# Ferramentas
# ----------------------------------------------------------------------
def buscar_noticias(tema: str) -> str:
    """Busca as 2 notícias mais recentes sobre um tema na NewsAPI."""
    resultado = newsapi.get_everything(
        q=tema,
        language="pt",
        sort_by="publishedAt",
        page_size=2,  # Quantidade de notícias
    )
    if resultado["status"] != "ok" or not resultado["articles"]:
        return f"Nenhuma notícia encontrada sobre '{tema}'."
    return "\n\n".join(
        f"{i}. {a['title']}\n   Fonte: {a['source']['name']}\n   Link: {a['url']}"
        for i, a in enumerate(resultado["articles"], 1)
    )


def enviar_noticia(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensagem}  # sem parse_mode: evita erro com _ e * nos títulos
    response = requests.post(url, json=payload)
    return response.json()


# ----------------------------------------------------------------------
# Módulo pesquisador
# ----------------------------------------------------------------------
class PesquisarNoticias(dspy.Signature):
    """Você é um pesquisador de notícias. Identifique o tema do pedido, use a
    ferramenta buscar_noticias e responda em português com um resumo curto de
    cada notícia, mantendo os links."""

    pedido: str = dspy.InputField(desc="Pedido do usuário, ex.: 'quero notícias sobre o mercado imobiliário'")
    resposta: str = dspy.OutputField(desc="Resumo das notícias encontradas")


class Pesquisador(dspy.Module):
    def __init__(self):
        super().__init__()
        self.agente = dspy.ReAct(PesquisarNoticias, tools=[buscar_noticias])

    def forward(self, pedido: str):
        resultado = self.agente(pedido=pedido)
        enviar_noticia(resultado.resposta)  # manda a resposta completa para o Telegram
        return resultado


if __name__ == "__main__":
    pesquisador = Pesquisador()
    pedido = input("O que você quer pesquisar? ")
    saida = pesquisador(pedido=pedido)
    print(saida.resposta)
#bolacha

