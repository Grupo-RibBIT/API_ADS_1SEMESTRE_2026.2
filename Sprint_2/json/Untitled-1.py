CAMINHO_JSON_VISTOS = "Sprint_2/json/imoveis_vistos.json"
LIMITE_IMOVEIS_VISTOS = 10

# Lock próprio: o lock_top_filtros não é reentrante e usá-lo aqui poderia causar deadlock
lock_vistos = threading.Lock()


def _carregar_vistos() -> dict:
    if not os.path.exists(CAMINHO_JSON_VISTOS):
        return {}
    with open(CAMINHO_JSON_VISTOS, "r", encoding="utf-8") as arquivo:
        try:
            return json.load(arquivo)
        except json.JSONDecodeError:
            return {}


def _salvar_vistos(dados_json: dict):
    os.makedirs(os.path.dirname(CAMINHO_JSON_VISTOS), exist_ok=True)
    with open(CAMINHO_JSON_VISTOS, "w", encoding="utf-8") as arquivo:
        json.dump(dados_json, arquivo, ensure_ascii=False, indent=2, default=str)


def registrar_imovel_visto(id_cliente, imovel: dict):
    '''Guarda o imóvel no topo da lista do cliente. Se já existia, ele apenas sobe para o topo.'''
    with lock_vistos:
        dados_json = _carregar_vistos()
        lista = dados_json.setdefault(str(id_cliente), [])
        lista[:] = [v for v in lista if v["id"] != imovel["id"]]
        imovel["data"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        lista.insert(0, imovel)
        del lista[LIMITE_IMOVEIS_VISTOS:]
        _salvar_vistos(dados_json)


def listar_imoveis_vistos(id_cliente, limite=5) -> list:
    with lock_vistos:
        return _carregar_vistos().get(str(id_cliente), [])[:limite]


def buscar_imovel_visto(id_cliente, imovel_id):
    for imovel in listar_imoveis_vistos(id_cliente, LIMITE_IMOVEIS_VISTOS):
        if imovel["id"] == imovel_id:
            return imovel
    return None


def formatar_imoveis_vistos(vistos: list) -> str:
    texto = "🏠 Últimos imóveis vistos:\n"
    for i, v in enumerate(vistos, start=1):
        valor = f"{v['valor']:,.0f}".replace(",", ".")
        texto += (
            f"{i}. {v['quartos']} quartos · {v['area']} m² · R$ {valor}\n"
            f"   {v['endereco']} ({v['data']})\n"
        )
    return texto