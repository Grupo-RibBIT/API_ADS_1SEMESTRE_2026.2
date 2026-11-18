
import json
import os
from collections import Counter

CAMINHO_JSON = "Sprint_2/json/histórico_cliente.json"


def carregar_dados():
    if not os.path.exists(CAMINHO_JSON):
        return {}

    try:
        with open(CAMINHO_JSON, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def salvar_dados(dados):
    os.makedirs(os.path.dirname(CAMINHO_JSON), exist_ok=True)

    with open(CAMINHO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


def ler_historico_json(id_cliente):
    dados = carregar_dados()
    return dados.get(str(id_cliente), [])


def salvar_mensagem_no_historico(id_cliente, mensagem):
    dados = carregar_dados()

    id_cliente = str(id_cliente)

    if id_cliente not in dados:
        dados[id_cliente] = []

    dados[id_cliente].append(mensagem)

    # Mantém apenas as últimas 10 pesquisas
    dados[id_cliente] = dados[id_cliente][-10:]

    salvar_dados(dados)


def exibir_historico(id_cliente):
    historico = ler_historico_json(id_cliente)

    if not historico:
        return "Você ainda não possui mensagens no histórico."

    texto = "📋 Histórico de pesquisas:\n\n"

    for i, pesquisa in enumerate(historico, start=1):
        if isinstance(pesquisa, dict):
            texto += (
                f"{i}. {pesquisa}\n"
            )
        else:
            texto += f"{i}. {pesquisa}\n"

    return texto


# função de análise do top filtros
# o top filtros agora refinado está pegando todas
# informações 

def obter_top_filtros():

    dados = carregar_dados()

    quartos = Counter()
    banheiros = Counter()
    vagas = Counter()
    tipos = Counter()
    bairros = Counter()
    precos = Counter()

    total_pesquisas = 0

    for historico in dados.values():

        for pesquisa in historico:

            # Ignora mensagens antigas em formato de texto
            if not isinstance(pesquisa, dict):
                continue

            total_pesquisas += 1

            if pesquisa.get("quartos") is not None:
                quartos[pesquisa["quartos"]] += 1

            if pesquisa.get("banheiros") is not None:
                banheiros[pesquisa["banheiros"]] += 1

            if pesquisa.get("vagas") is not None:
                vagas[pesquisa["vagas"]] += 1

            if pesquisa.get("tipo"):
                tipos[pesquisa["tipo"]] += 1

            if pesquisa.get("bairro"):
                bairros[pesquisa["bairro"]] += 1

            if pesquisa.get("preco_maximo") is not None:
                precos[pesquisa["preco_maximo"]] += 1

    if total_pesquisas == 0:
        return "Ainda não existem pesquisas suficientes para gerar os top filtros."

    texto = "📊 Top filtros mais pesquisados\n\n"

    texto += f"🔎 Total de pesquisas analisadas: {total_pesquisas}\n\n"

    def adicionar_ranking(titulo, contador, unidade=""):
        nonlocal texto

        texto += f"{titulo}\n"

        if not contador:
            texto += "Nenhum dado disponível.\n\n"
            return

        for valor, quantidade in contador.most_common(3):
            texto += f"• {valor} {unidade}: {quantidade} pesquisas\n"

        texto += "\n"

    adicionar_ranking("🛏️ QUARTOS", quartos, "quartos")
    adicionar_ranking("🚿 BANHEIROS", banheiros, "banheiros")
    adicionar_ranking("🚗 VAGAS DE GARAGEM", vagas, "vagas")
    adicionar_ranking("🏠 TIPOS DE IMÓVEL", tipos)
    adicionar_ranking("📍 BAIRROS MAIS PROCURADOS", bairros)

    texto += "💰 Faixas de preço mais pesquisadas\n"

    if precos:
        for valor, quantidade in precos.most_common(3):
            texto += (
                f"• Até R$ {valor:,.2f}: "
                f"{quantidade} pesquisas\n"
            )
    else:
        texto += "Nenhum dado disponível.\n"

    return texto



@bot.message_handler(commands=["historico"])
def mostrar_historico(message):

    id_cliente = str(message.from_user.id)

    historico = exibir_historico(id_cliente)

    bot.reply_to(message, historico)


@bot.message_handler(commands=["topfiltros"])
def mostrar_top_filtros(message):

    resultado = obter_top_filtros()

    bot.reply_to(message, resultado)

