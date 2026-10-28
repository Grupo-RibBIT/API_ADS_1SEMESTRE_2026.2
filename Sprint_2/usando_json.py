import json
import os
from datetime import datetime
import threading

CAMINHO_JSON_HISTÓRICO = "Sprint_2/json/histórico_cliente.json"

CAMINHO_JSON_TOP_FILTROS = "Sprint_2/json/top_filtros.json"

lock_top_filtros = threading.Lock()

def ler_histórico_json(id_cliente) -> list:
    with lock_top_filtros:
        if not os.path.exists(CAMINHO_JSON_HISTÓRICO):
            return []

        with open(CAMINHO_JSON_HISTÓRICO, "r", encoding="utf-8") as arquivo:
            try:
                dados_json = json.load(arquivo)
            except json.JSONDecodeError:
                return []

        return dados_json.get(str(id_cliente), [])


def salvar_mensagem_no_histórico(id_cliente, mensagem):
    with lock_top_filtros:
        if os.path.exists(CAMINHO_JSON_HISTÓRICO):
            with open(CAMINHO_JSON_HISTÓRICO, "r", encoding="utf-8") as arquivo:
                try:
                    dados_json = json.load(arquivo)
                except json.JSONDecodeError:
                    dados_json = {}
        else:
            dados_json = {}

        id_cliente = str(id_cliente)

        if id_cliente not in dados_json:
            dados_json[id_cliente] = []

        dados_json[id_cliente].append(mensagem)

        # Mantém apenas as últimas 10 mensagens
        dados_json[id_cliente] = dados_json[id_cliente][-10:]

        with open(CAMINHO_JSON_HISTÓRICO, "w", encoding="utf-8") as arquivo:
            json.dump(dados_json, arquivo, ensure_ascii=False, indent=2)


def exibir_historico(id_cliente) -> str:
    historico = ler_histórico_json(id_cliente)

    if not historico:
        return "Você ainda não possui mensagens no histórico."

    texto = "Histórico de mensagens:\n\n"

    for i, mensagem in enumerate(historico, start=1):
        texto += f"{i}. {mensagem}\n"

    return texto


def registrar_filtros_no_ranking(filtros_pesquisados):
    '''Soma 1 no contador de cada filtro pesquisado dentro do JSON de ranking'''
    with lock_top_filtros:
        with open(CAMINHO_JSON_TOP_FILTROS, "r", encoding="utf-8") as topf:
            ranking = json.load(topf)
        
        json_atualizado = False
        
        for item_pesquisado in filtros_pesquisados:
            for item in ranking["filtros"]:
                if item["filtro"] == item_pesquisado:
                    item["pesquisas"] += 1
                    print(item_pesquisado, "foi encontrado! Um contador foi adicionado no item ", item["filtro"], "do JSON")
                    json_atualizado = True
                    break
            
            if json_atualizado == False:
                print("Filtro não encontrado: ", item_pesquisado)
            
        if json_atualizado:
            ranking["ultima_atualizacao"] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            with open(CAMINHO_JSON_TOP_FILTROS, "w", encoding="utf-8") as topf:
                json.dump(ranking, topf, indent=2, ensure_ascii=False)
            print("Ranking de Filtros atualizado!")
        else:
            print("Nada foi alterado.")


def ler_top_filtros():
    with lock_top_filtros:
        with open(CAMINHO_JSON_TOP_FILTROS, "r", encoding="utf-8") as topf:
            ranking = json.load(topf)

        return ranking

            
