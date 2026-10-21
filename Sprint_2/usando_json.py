import json

#Estrutura do json do histórico do cliente {id_cliente:[mensagem1,mensagem2,mensagem3,...]}



def ler_histórico_json(id_cliente) -> list:
    dados_json = {}
    with open("Sprint_2/json/histórico_cliente.json","r",encoding="utf-8") as arquivo:    
        dados_json = json.load(arquivo)

    histórico_mensagem = dados_json[id_cliente]

    return histórico_mensagem


def salvar_mensagem_no_histórico(id_cliente,mensagem):
    dados_json = {}
    with open("Sprint_2/json/histórico_cliente.json","r",encoding="utf-8") as arquivo:    
        dados_json = json.load(arquivo)

    if id_cliente not in dados_json.keys():
        dados_json[id_cliente] = [mensagem]
    else:
        if len(dados_json[id_cliente]) < 10:
            dados_json[id_cliente].append(mensagem)
        else:
            dados_json[id_cliente].pop(0)
            dados_json[id_cliente].append(mensagem)

    with open("Sprint_2/json/histórico_cliente.json","w",encoding="utf-8") as arquivo:
        json.dump(dados_json, arquivo, ensure_ascii=False, indent=2)


#Exemplos para ver funcionando

salvar_mensagem_no_histórico("tetstetstete","AAAAAAA")

print(ler_histórico_json("tetstetstete"))

salvar_mensagem_no_histórico("tetstetstete","BBBBBBB")

print(ler_histórico_json("tetstetstete"))

salvar_mensagem_no_histórico("asdnldasdw","CCCCCCC")

