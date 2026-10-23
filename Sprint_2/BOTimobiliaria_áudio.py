# Biblioteca que o código está usando
import dspy
import telebot
import random
import re  # Biblioteca de Expressões Regulares (usada para extrair números de textos)
import pandas as pd  # Biblioteca para manipulação de dados e leitura do arquivo CSV
import time
from typing import Literal
import os
import whisper
import numpy as np
from pydub import AudioSegment

from geopy.geocoders import Nominatim

#Configuração do Bot/Telegram e do LLM

API_TOKEN = '8996078250:AAEUE_ZB-zEMCLqs0opeT6up2zcl1MWbRQA'
bot = telebot.TeleBot(API_TOKEN)


lm = dspy.LM('ollama_chat/qwen2.5-coder:7b', api_base='http://localhost:11434', api_key='ignored')
dspy.configure(lm=lm)

geolocator = Nominatim(user_agent="Bottelegram")

modelo_whisper = whisper.load_model("small")

#Dados externos

list_fotos_apt = ["kamen-nikolov-fin","maxim-dorokhov","valmik-shah"]

path_csv = "apartamentos_sp_estruturado.csv"

TiposFiltro = Literal["preço_num","Área","Endereço","Quartos","Banheiros","Vagas_de_estacionamento"]

está_rodando = False

#Fazendo o dataframe do panda
def transforma_csv_em_dataFrame(caminho_csv):
  df = pd.read_csv(caminho_csv)
  return df

df = transforma_csv_em_dataFrame(caminho_csv=path_csv)

def corrigindo_preço_dataFrame(p_df):
  #p_df = p_df.dropna(subset=["Preço"])
  p_df["preço_num"] = (
    p_df["Preço"]
    .astype(str)
    .str.replace(r"[^\d,.]", "", regex=True)
    .str.replace(".", "", regex=False)
    .str.replace(",", "", regex=False)
  )
  p_df["preço_num"] = pd.to_numeric(p_df["preço_num"])
  #p_df = p_df.dropna(subset=["preço_num"])
  return p_df

df = corrigindo_preço_dataFrame(df)

# Lista para armazenar o histórico recente das mensagens
historico_conversa = []

#Definindo e estruturando as entradas e saídas dos sub-modulos

class DescriçãoApartamento(dspy.Signature):
  '''Traduz a linha do csv do apartamento achado em caracteristicas do apartamento'''
  linha_do_csv:str = dspy.InputField(desc="Linha que foi encontrada pela filtragem do csv")
  banheiros:int = dspy.OutputField()
  quartos:int = dspy.OutputField()
  área:int = dspy.OutputField()
  valor:float = dspy.OutputField()
  estacionamento:int = dspy.OutputField()
  endereço_apartamento:str = dspy.OutputField()

class CaracterísticasApresentação(dspy.Signature):
  '''Recebe as características específicas do apartamento e monta uma apresentação'''
  chat_id_telegram = dspy.InputField(desc="Identificador do usuário que mandou a mensagem no telegram")
  banheiros:int = dspy.InputField()
  quartos:int = dspy.InputField()
  área:int = dspy.InputField()
  valor:float = dspy.InputField(desc="Usando os pontos de milhar no padrão brasileiro")
  estacionamento:int = dspy.InputField()
  fotos = dspy.InputField()
  apresentação:str = dspy.OutputField(desc="Apresentação seguindo o modelo definido pela ferramenta 'montar_mini_apresentação'")

class EscolhasAtendente(dspy.Signature):
  '''Simula a resposta de um atendente de imobiliária que recebe a mensagem do cliente e extrai oque ele deseja'''
  mensagem_do_cliente:str = dspy.InputField()
  chat_id_telegram = dspy.InputField(desc="Identificador do usuário que mandou a mensagem no telegram")
  desejo_do_cliente:str = dspy.OutputField(desc="Oque o cliente quer com essa conversa, para ser usado internamente")


class EscolhasGerenciador(dspy.Signature):
  '''Analisa o desejo_do_cliente extraído pelo Atendente e classifica com Bool (True ou False) se a mensagem possui as palavras apresentação e/ou localização e/ou um imóvel
  REGRAS:
    - Se o cliente "QUER UM APARTAMENTO" ele deseja também uma apresentação
  '''
  analisar_escopo:str = dspy.InputField()
  lista_de_ferramentas:list = dspy.InputField(desc="Lista de ferramentas usadas pelos sub-modulos")
  precisa_de_localizacao:bool = dspy.OutputField(desc="Define se o cliente mencionou/pediu localização de um imóvel, que precisará ser enviada")
  precisa_de_apresentacao:bool = dspy.OutputField(desc="Define se o cliente mencionou/pediu a apresentação ou mini-apresentação de um imóvel, que precisará ser enviada")
  precisa_de_busca_no_csv:bool = dspy.OutputField(desc="Define se o cliente mencionou/pediu um imóvel, uma rua, um bairro, ou uma informação sobre um imóvel, que precisará ser buscada no csv")

class ExtrairFiltros(dspy.Signature):
  """Extrai filtros de busca de imóveis a partir do pedido do usuário.
  
    REGRAS:
      - Não usar variáveis None
      -Não usar 'float('inf')' nos valores desejados
  """
  texto_usuario: str = dspy.InputField()
  tipos_de_filtro: list[TiposFiltro] = dspy.OutputField(desc="Lista com os tipos de filtragem/colunas do CSV,sendo 'Área' a área últil construida do apartamento")
  valor_desejado: dict[TiposFiltro,list] = dspy.OutputField(desc="Valores desejados do cliente com base nos tipos de filtro, se tiver apenas um valor, é um intervalo de 0 até o valor pedido. Se tiver mais de uma variável é um intervalo que engloba esses valores")

# Adicionado: assinatura DSPy usada exclusivamente para criar a mensagem do /start.
# Ela separa as informações fornecidas pelo código da redação produzida pela IA.
class BoasVindasAssistente(dspy.Signature):
  """Gera uma saudação variada, mas limitada às funcionalidades reais do bot."""
  #a IA recebe uma lista autorizada e deve limitar a apresentação a esses filtros.
  filtros_disponiveis: list[str] = dspy.InputField(
      desc="Lista fechada de filtros realmente disponíveis no código. Não invente outros."
  )
  #define o objetivo geral do bot para evitar promessas de funcionalidades inexistentes.
  funcionalidades: str = dspy.InputField(
      desc="O bot pesquisa imóveis para compra a partir das características informadas pelo usuário."
  )
  #este é o texto final que o Handler enviará ao usuário no Telegram.
  mensagem_boas_vindas: str = dspy.OutputField(
      desc="Saudação breve em português brasileiro, explicando como começar uma pesquisa."
  )

class FiltrosDoCSV(dspy.Signature):
  '''Acha apartamentos que se encaixam no requisitos do cliente dentro do csv'''
  df_bruto = dspy.InputField(desc="Dataframe completo dos apartamentos")
  tipos_de_filtro: list[TiposFiltro] = dspy.InputField(desc="Lista com os tipos de filtragem/colunas do CSV, sendo 'Área' a área útil construída do apartamento")
  valor_desejado: dict[TiposFiltro,list] = dspy.InputField(desc="Valores desejados do cliente, se tiver mais de uma variável é um intervalo que engloba esses valores. Se tiver apenas um valor, é um intervalo de 0 até o valor pedido.")
  lista_apartamentos_str:list = dspy.OutputField(desc="Lista dos apartamentos achados pelo filtro em formato de sting")


# Qwen redige mensagens naturais para a navegação. As contagens são
# calculadas pelo Python e fornecidas ao modelo para evitar números inventados.
class MensagemInteracao(dspy.Signature):
  """Escreve uma mensagem curta, natural e cordial para o cliente da imobiliária."""
  objetivo: str = dspy.InputField(desc="O que a mensagem precisa comunicar")
  total_encontrado: int = dspy.InputField(desc="Total de imóveis na busca atual")
  apresentados_nesta_resposta: int = dspy.InputField(desc="Quantidade apresentada nesta resposta")
  restantes: int = dspy.InputField(desc="Quantidade ainda não apresentada")
  mensagem: str = dspy.OutputField(desc="Mensagem em português brasileiro; não invente números")


#Lista de feramentas/funções para serem usadas pelos sub-modulos

def salvar_no_historico(chat_id_telegram, texto: str):
  """
  Adiciona uma nova mensagem ao histórico do sistema e garante que
  o limite máximo de 10 mensagens armazenadas seja respeitado.
  """
  # Insere a mensagem formatada no final da lista
  historico_conversa.append(f"{chat_id_telegram}: {texto}")

  # Se a lista ultrapassar 10 itens, remove o item mais antigo (primeiro elemento)
  if len(historico_conversa) > 10:
      historico_conversa.pop(0)

def mandar_mensagem_pelo_telegram(mensagem_text:str,chat_id_telegram:str|int):
  '''Manda mensagem para o cliente,identificado pelo chat_id, atraves do telegram'''
  bot.send_message(chat_id = chat_id_telegram,text=mensagem_text)
  return f"Mensagem dizendo: '{mensagem_text}' foi enviada para o cliente "


def montar_mini_apresentação_e_mandar_pelo_telegram(
    fotos: str,
    num_banheiros:int, 
    num_quartos:int, 
    num_estacionamento:int, 
    área:int, 
    valor:int, 
    chat_id_telegram):
  
  '''Monta e Envia a apresentação do apartamento para o cliente dentro do telegram'''
  
  bot.send_message_draft(chat_id_telegram,20,"")

  modelo_layout = f'''
  <tg-slideshow>

  ![](https://raw.githubusercontent.com/Grupo-RibBIT/arquivo-base/refs/heads/main/fotos_exemplo_apt/{fotos}-1.jpg)
  ![](https://raw.githubusercontent.com/Grupo-RibBIT/arquivo-base/refs/heads/main/fotos_exemplo_apt/{fotos}-2.jpg)
  ![](https://raw.githubusercontent.com/Grupo-RibBIT/arquivo-base/refs/heads/main/fotos_exemplo_apt/{fotos}-3.jpg)

  </tg-slidehow>

  #Apartamento ID563595
  ######Valor de Compra: ==R${valor}==

  | Infos do Apartamento | |
  |:---------|:--------:|
  | Área Útil| {área} m² |
  | Quartos | {num_quartos} (1 suíte) |
  | Banheiros | {num_banheiros} |
  | Vagas de Estacionamento | {num_estacionamento} |

  ###Destaques:
  - Tem piscina
  >**Para mais informações**: [Site da Imobiliária](https://github.com/Grupo-RibBIT)
  '''

  apresentação = telebot.types.InputRichMessage(markdown=modelo_layout)

  bot.send_rich_message(chat_id_telegram,apresentação)
  return "Apresentação enviada com sucesso"

def enviar_localizacao_no_telegram(endereço_apartamento, chat_id_telegram):
  '''Peqsuisa o endereço_apartamento no OpenStreetMaps e usa as coordenadas para enviar a localização no telegram'''
  endereco = geolocator.geocode(endereço_apartamento)
  print('Geocode: ', endereco)
  if endereco:
      def send_coords():
          bot.send_message(chat_id=chat_id_telegram, text='Localização aproximada: ')
          bot.send_location(
              chat_id=chat_id_telegram,
              latitude=endereco.latitude,
              longitude=endereco.longitude)
          return 'Enviado.'
      print('Endereco: ', endereco.address)
      print('Latitude: ', endereco.latitude)
      print('Longitude: ', endereco.longitude)
  else:
      return 'Endereço nao encontrado, encerre a pesquisa e peça para o usuario colocar um endereço válido' 
  return send_coords()


def transformar_dataframe_para_string(df_filtrado):
  '''Transforma o dataFrame filtrado em uma lista com os apartamentos encontrados'''
  apartamentos_encontrados = []
  for idx, (_, linha) in enumerate(df_filtrado.iterrows(), 1):
    linha_csv_str = linha.to_frame().T.to_csv(index=False)
    apartamentos_encontrados.append(linha_csv_str)
  return apartamentos_encontrados
   

#Filtros Csv
def filtrar_csv(tipo_de_filtragem,df_bruto,valores_desejados:dict[TiposFiltro,list]):
  '''Filtra o DataFrame pelo tipo de filtragem escolhido determinado valor/intervalo de valores desejado pelo cliente'''
  df = df_bruto
  print("Vai filtrar usando: ",tipo_de_filtragem)
  for tipo in tipo_de_filtragem:
    print("Pegou o filtro atual: ",tipo)
    df = df.dropna(subset=[tipo])
    print("Os valores desejados são: ",valores_desejados)
    valores_desejado_atual= valores_desejados[tipo]
    if tipo == "Endereço":
      df = df[
          df[tipo]
          .astype(str)
          .str.contains(valores_desejado_atual[0], case=False, na=False)
      ]
    elif tipo == "preço_num":
      if len(valores_desejado_atual) >= 2:
          v_min, v_max = min(valores_desejado_atual[0], valores_desejado_atual[1]), max(
              valores_desejado_atual[0], valores_desejado_atual[1]
          )
          df = df[
              (df[tipo] >= v_min) & (df[tipo] <= v_max)
          ]
      else:
          v_min, v_max = 0, max(
              valores_desejado_atual
          )
          df = df[
              (df[tipo] >= v_min) & (df[tipo] <= v_max)
          ]
    else:
      if len(valores_desejado_atual) >= 2:
                v_min, v_max = min(valores_desejado_atual[0], valores_desejado_atual[1]), max(
                    valores_desejado_atual[0], valores_desejado_atual[1]
                )
                df = df[
                    (df[tipo] >= v_min) & (df[tipo] <= v_max)
                ]
      else:
          df = df[df[tipo] == valores_desejado_atual[0]]

  if not df.empty:
    print(f"[Filtro CSV] {df.shape[0]} imóveis retornados.")
  else:
    print("[Filtro CSV] Nenhum imóvel encontrado para estes critérios.")

  return df



#Lista de ferramentas para o Gerenciador
ferramentas_dos_modulos = [mandar_mensagem_pelo_telegram, 
                           montar_mini_apresentação_e_mandar_pelo_telegram, 
                           enviar_localizacao_no_telegram, 
                           mandar_mensagem_pelo_telegram, 
                           filtrar_csv, 
                           transformar_dataframe_para_string,
                           ]

# ADICIONADO: aplica filtros adicionais à seleção atual sem tocar no DataFrame original.
# Para campos de contagem (quartos, banheiros e vagas), um único valor é tratado como
# correspondência exata; para preço, área e endereço, preserva-se a regra já existente.
def aplicar_filtros_adicionais(df_atual, tipos_de_filtro, valores_desejados):
  df_refinado = df_atual.copy()
  campos_contagem = {"Quartos", "Banheiros", "Vagas_de_estacionamento"}
  for tipo in tipos_de_filtro:
    valores = valores_desejados[tipo]
    if tipo in campos_contagem and len(valores) == 1:
      df_refinado = df_refinado.dropna(subset=[tipo])
      df_refinado = df_refinado[df_refinado[tipo] == valores[0]]
    else:
      # Reutiliza o filtro original para intervalos, preço, área e endereço.
      df_refinado = filtrar_csv([tipo], df_refinado, {tipo: valores})
  return df_refinado


# ADICIONADO: guarda a pesquisa ativa e o progresso da paginação de cada chat.
# O DataFrame original permanece intacto; cada estado guarda apenas o resultado da busca.
estados_pesquisa = {}

# ADICIONADO: limite centralizado para facilitar a alteração futura da quantidade por resposta.
IMOVEIS_POR_RESPOSTA = 3

#Criação do Modulo Geral

class BotImobiliária(dspy.Module):
  def __init__(self,dataframe):
    super().__init__()

    self.dataframe = dataframe

    #Definindo os sub-modulos

    self.gerenciador = dspy.ChainOfThought(EscolhasGerenciador)

    self.atendente = dspy.ChainOfThought(EscolhasAtendente)

    self.extrator = dspy.ChainOfThought(ExtrairFiltros)

    self.arquiteto = dspy.ChainOfThought(DescriçãoApartamento)

    self.apresentador = dspy.ReAct(CaracterísticasApresentação, tools=[montar_mini_apresentação_e_mandar_pelo_telegram])

    self.navegador = dspy.ReAct("endereço_apartamento, chat_id_telegram -> localização", tools=[enviar_localizacao_no_telegram], max_iters=1)

    self.finalizador = dspy.ReAct("resultado_do_pensamento -> resposta_final_cliente",tools=[])

    # ADICIONADO: módulo de linguagem usado para redigir mensagens de navegação.
    self.mensageiro = dspy.Predict(MensagemInteracao)

  # ADICIONADO: apresenta até três imóveis da pesquisa guardada, sem refazer a busca.
  def apresentar_lote(self, chat_id_telegram, estado, precisa_de_localizacao=False):
    print("Começando a apresentação dos lotes...")
    resultados = estado["resultados"]
    total = len(resultados)
    inicio_lote = estado["proximo_indice"]
    fim_lote = min(inicio_lote + IMOVEIS_POR_RESPOSTA, total)
    lote = resultados.iloc[inicio_lote:fim_lote]
    quantidade_apresentada = len(lote)

    # ADICIONADO: avança o índice para a próxima página antes de enviar as apresentações.
    estado["proximo_indice"] = fim_lote

    # ADICIONADO: reaproveita o arquiteto e o apresentador existentes para cada imóvel do lote.
    for _, linha in lote.iterrows():
      linha_achada = linha.to_frame().T.to_csv(index=False)
      caracteristicas = self.arquiteto(linha_do_csv=linha_achada)
      print(caracteristicas)
      foto_escolhida = random.randint(0, len(list_fotos_apt) - 1)
      slides = list_fotos_apt[foto_escolhida]
      montar_mini_apresentação_e_mandar_pelo_telegram(
        fotos=slides,
        num_banheiros=caracteristicas.banheiros,
        num_quartos=caracteristicas.quartos,
        área=caracteristicas.área,
        valor=caracteristicas.valor,
        num_estacionamento=caracteristicas.estacionamento,
        chat_id_telegram=chat_id_telegram
      )

      # ALTERADO: a localização Geopy faz parte da apresentação de CADA imóvel.
      # A ordem é: apresentar o imóvel atual, enviar sua localização e só então
      # passar ao próximo imóvel do lote. A chamada direta garante que a função
      # que usa o Geopy seja executada, sem depender do agente ReAct decidir usá-la.
      try:
        enviar_localizacao_no_telegram(
          endereço_apartamento=caracteristicas.endereço_apartamento,
          chat_id_telegram=chat_id_telegram
        )
      except Exception as erro_localizacao:
        # ALTERADO: uma falha de geocodificação não deve impedir os próximos imóveis.
        print(f"Erro ao enviar localização do imóvel: {erro_localizacao}")
        bot.send_message(
          chat_id_telegram,
          "Não consegui localizar este endereço no mapa, mas vou continuar com os próximos imóveis."
        )

    # ADICIONADO: Python calcula os números; o modelo apenas os transforma em uma mensagem natural.
    restantes = max(total - fim_lote, 0)
    if total == 0:
      objetivo = "Informe naturalmente que nenhum imóvel corresponde aos critérios atuais e sugira ajustar filtros ou iniciar nova pesquisa."
    elif restantes > 0:
      objetivo = f"Informe exatamente estes números, sem alterá-los: total encontrado={total}; apresentados nesta resposta={quantidade_apresentada}; ainda não apresentados={restantes}. Explique isso naturalmente e convide o cliente a escolher um dos botões."
    else:
      objetivo = f"Informe exatamente estes números, sem alterá-los: total encontrado={total}; apresentados nesta resposta={quantidade_apresentada}; ainda não apresentados={restantes}. Avise que não há mais imóveis para mostrar e sugira ajustar filtros ou iniciar nova pesquisa."

    texto_resultados = self.mensageiro(
      objetivo=objetivo,
      total_encontrado=total,
      apresentados_nesta_resposta=quantidade_apresentada,
      restantes=restantes
    ).mensagem

    # ADICIONADO: os três botões permanecem disponíveis após cada lote, conforme solicitado.
    # Se não houver mais imóveis, o callback de "Mostrar Próximos" informa que a lista terminou.
    teclado = telebot.types.InlineKeyboardMarkup(row_width=1)
    teclado.add(
      telebot.types.InlineKeyboardButton("Acrescentar Filtro", callback_data="imob_filtro"),
      telebot.types.InlineKeyboardButton("Mostrar Próximos", callback_data="imob_proximos"),
      telebot.types.InlineKeyboardButton("Nova Pesquisa", callback_data="imob_nova")
    )
    bot.send_message(chat_id_telegram, texto_resultados, reply_markup=teclado)

  #A função foward diz como o modulo geral vai funcionar

  def forward(self, mensagem) -> dspy.Prediction:
    global está_rodando
    está_rodando = True

    inicio = time.time()
    resposta_inicial = self.atendente(mensagem_do_cliente=mensagem.text,chat_id_telegram=mensagem.chat.id)
    fim = time.time()
    print(f"Resposta Atendente obtida em {fim - inicio:.2f} segundos")
    print(resposta_inicial)

    inicio = time.time()
    escopo_do_pedido = self.gerenciador(analisar_escopo = resposta_inicial.desejo_do_cliente, lista_de_ferramentas=ferramentas_dos_modulos)
    fim = time.time()
    print(f"Escopo obtido em {fim - inicio:.2f} segundos")
    print('Escopo Pedido:', escopo_do_pedido)

    linha_de_pensamento = f'''
          ##Resposta Momentânea
            {resposta_inicial}
          ##Escopo Definido
            {escopo_do_pedido}
          
          '''

    if escopo_do_pedido.precisa_de_busca_no_csv == True:
        inicio = time.time()
        filtros_de_pesquisa = self.extrator(texto_usuario=mensagem.text)
        fim = time.time()
        print(f"Filtros obtidos em {fim - inicio:.2f} segundos")
        print(filtros_de_pesquisa)

        todos_os_filtros = ["preço_num","Área","Endereço","Quartos","Banheiros","Vagas_de_estacionamento"]
        filtros_não_usados = [filtro for filtro in todos_os_filtros if filtro not in filtros_de_pesquisa.tipos_de_filtro]
        print("Filtros que não foram usados: ", filtros_não_usados) 

        inicio = time.time()
        apartamentos_achados = filtrar_csv(tipo_de_filtragem=filtros_de_pesquisa.tipos_de_filtro,valores_desejados=filtros_de_pesquisa.valor_desejado,df_bruto=self.dataframe)
        fim = time.time()
        print(f"Apartamentos obtidos em {fim - inicio:.2f} segundos")
        print(apartamentos_achados)

        print(f"Foram achados {apartamentos_achados.shape[0]} apartamentos com essa busca")
        
        if apartamentos_achados.shape[0] > 30:
          bot.send_message(mensagem.chat.id,f"Foram encontrados muitos ({apartamentos_achados.shape[0]}) apartamentos com as características que você procura, precisamos de informações extras para sermos mais precisos!")
          bot.send_message(mensagem.chat.id,f"Você tem preferência sobre {", ".join(filtros_não_usados)}?")
          return


        # ADICIONADO: guarda o resultado completo para paginação e filtros adicionais.
        # A cópia evita que alterações na pesquisa atual modifiquem o DataFrame original.
        estado = {
        "resultados": apartamentos_achados.copy(),
        "proximo_indice": 0,
        "filtros": list(filtros_de_pesquisa.tipos_de_filtro),
        "valores_filtros": dict(filtros_de_pesquisa.valor_desejado),
        "precisa_de_localizacao": bool(escopo_do_pedido.precisa_de_localizacao),
        "aguardando_filtro": False,
        "aguardando_nova_pesquisa": False
        }

        print("Estado atual: ", estado)
        
        estados_pesquisa[mensagem.chat.id] = estado
    
        # ADICIONADO: a primeira resposta apresenta somente três imóveis.
        self.apresentar_lote(mensagem.chat.id, estado, estado["precisa_de_localizacao"])
        está_rodando = False
        return dspy.Prediction("Busca realizada e primeiro lote apresentado.")

    # Comportamento anterior mantido para mensagens que não iniciam uma busca no CSV.
    linha_de_pensamento = f"""
      ##Resposta Momentânea
      {resposta_inicial}
      ##Escopo Definido
      {escopo_do_pedido}
    """


    print(linha_de_pensamento)

    final = self.finalizador(resultado_do_pensamento=linha_de_pensamento).resposta_final_cliente
    
    está_rodando = False
    return dspy.Prediction(final)

#Criando uma instância do modulo geral
bot_recepção = BotImobiliária(dataframe=df)

#NOVO: lista central dos filtros que a saudação está autorizada a mencionar.
# Importante: manter esta lista sincronizada com os filtros realmente aceitos pelo código.
FILTROS_DISPONIVEIS_START = [
    "Preço",
    "Área útil",
    "Endereço",
    "Quartos",
    "Banheiros",
    "Vagas de estacionamento",
]


# Cria o preditor da saudação separado dos preditores usados para pesquisar imóveis.
# Assim, o /start não precisa chamar nem modificar o fluxo de pesquisa.
boas_vindas_ia = dspy.Predict(BoasVindasAssistente)


# NOVO: Handler independente para o comando /start do Telegram.
# Ele só recebe o usuário e apresenta as funcionalidades; não pesquisa nem filtra imóveis.
# Deve ficar antes do Handler genérico abaixo, para que /start não caia no fluxo normal.
@bot.message_handler(commands=["start"])
def iniciar_conversa(message):
  # NOVO: tenta gerar uma saudação com a IA local, para que seja mais fluido.
  try:
    resposta = boas_vindas_ia(
        filtros_disponiveis=FILTROS_DISPONIVEIS_START,
        # Estas instruções acompanham a lista fechada e restringem o conteúdo da resposta.
        funcionalidades=(
            "O assistente pesquisa imóveis para compra a partir das características informadas. "
            "Só pode mencionar os filtros listados em filtros_disponiveis. "
            "Não diga que já pesquisou ou encontrou imóveis. "
            "Convide o usuário a descrever o imóvel que procura."
        ),
    )
    # Remove espaços extras antes de enviar a mensagem ao Telegram.
    texto = resposta.mensagem_boas_vindas.strip()
    if not texto:
      raise ValueError("A IA retornou uma mensagem de boas-vindas vazia.")
  except Exception as erro:
    # NOVO: alternativa caso o Ollama falhe, demore ou retorne uma resposta vazia.
    # A recepção continua funcionando mesmo quando não é possível usar a IA.
    print(f"Erro ao gerar boas-vindas com a IA: {erro}")
    texto = (
        "Olá! Bem-vindo ao Assistente Imobiliário! 🏡\n\n"
        "Posso ajudar a pesquisar imóveis para compra. Você pode informar "
        "preço, área útil, endereço, quartos, banheiros e vagas de estacionamento.\n\n"
        "Conte como é o imóvel que você está procurando para começarmos."
    )

  # NOVO: envia a saudação ao mesmo chat que executou o comando /start.
  bot.send_message(message.chat.id, texto)

# ADICIONADO: callbacks dos botões inline de navegação dos resultados.
@bot.callback_query_handler(func=lambda call: call.data in {"imob_filtro", "imob_proximos", "imob_nova"})
def tratar_botoes_resultados(call):
  chat_id = call.message.chat.id

  # ALTERADO: tenta confirmar o clique imediatamente, antes de qualquer operação
  # que possa demorar (IA, filtros ou geocodificação). Um callback pode já ter
  # expirado quando o Telegram o entrega; nesse caso, registramos o erro e seguimos.
  try:
    bot.answer_callback_query(call.id)
  except Exception as erro_callback:
    print(f"Aviso ao confirmar clique do botão: {erro_callback}")

  # ADICIONADO: remove os três botões da mensagem clicada para evitar teclados antigos.
  # A remoção é independente da ação escolhida e não apaga a mensagem nem os imóveis.
  try:
    bot.edit_message_reply_markup(
      chat_id=chat_id,
      message_id=call.message.message_id,
      reply_markup=None
    )
  except Exception as erro_teclado:
    # Se a mensagem já não tiver teclado ou não puder ser editada, a ação ainda continua.
    print(f"Aviso ao remover teclado inline: {erro_teclado}")

  estado = estados_pesquisa.get(chat_id)

  if call.data == "imob_proximos":
    # ADICIONADO: apresenta o próximo lote da mesma pesquisa, sem reler ou refiltrar o CSV.
    if not estado:
      bot.send_message(chat_id, "Não encontrei uma busca ativa. Envie sua pesquisa para começarmos.")
      return
    if estado["proximo_indice"] >= len(estado["resultados"]):
      bot.send_message(chat_id, "Você já viu todos os imóveis encontrados. Se quiser, pode iniciar uma nova pesquisa.")
      return
    bot_recepção.apresentar_lote(chat_id, estado, estado["precisa_de_localizacao"])
    return

  if call.data == "imob_filtro":
    # ADICIONADO: a próxima mensagem de texto será interpretada como filtro para a busca atual.
    if not estado:
      bot.send_message(chat_id, "Ainda não há uma busca ativa. Envie primeiro os critérios dos imóveis que procura.")
      return
    estado["aguardando_filtro"] = True
    estado["aguardando_nova_pesquisa"] = False
    mensagem = bot_recepção.mensageiro(
      objetivo="Pergunte de forma natural e cordial qual filtro o cliente quer acrescentar para refinar a busca atual. Não diga que o filtro já foi aplicado.",
      total_encontrado=len(estado["resultados"]),
      apresentados_nesta_resposta=0,
      restantes=max(len(estado["resultados"]) - estado["proximo_indice"], 0)
    ).mensagem
    bot.send_message(chat_id, mensagem)
    return

  if call.data == "imob_nova":
    # ADICIONADO: limpa a pesquisa deste chat, preservando o DataFrame original carregado do CSV.
    estados_pesquisa[chat_id] = {
      "resultados": pd.DataFrame(),
      "proximo_indice": 0,
      "filtros": [],
      "valores_filtros": {},
      "precisa_de_localizacao": False,
      "aguardando_filtro": False,
      "aguardando_nova_pesquisa": True
    }
    mensagem = bot_recepção.mensageiro(
      objetivo="Convide o cliente, de forma natural e cordial, a descrever o que deseja procurar na nova pesquisa, sabendo que essa não esta sendo a sua primeira busca.",
      total_encontrado=0,
      apresentados_nesta_resposta=0,
      restantes=0
    ).mensagem
    bot.send_message(chat_id, mensagem)

def processar_mensagem(message):
   try:
      print(f"Mensagem incaminhada para o DSPy!!")
      print(f"Mensagem recebida: {message.text}")

      salvar_no_historico(message.chat.id, message.text)

      resultado_interação = bot_recepção(mensagem=message)

      print(f"DSPY terminou o processamento.!")

      resposta = getattr(resultado_interação, "final", None)

      if resposta:
          bot.send_message(message.chat.id, str(resposta))
          return resultado_interação

   except Exception as e:
        print(f"[Erro no processamento!] {e}")
        bot.send_message(message.chat.id, "Não consegui processar a mensagem, por favor tente de novo")
        return None

def transcrever_audio_whisper(caminho_arquivo: str) -> str:
    """Padroniza o áudio em memória (16kHz Mono PCM 16-bit) e realiza a transcrição
       otimizada usando o modelo Whisper."""
    
    # Carrega o arquivo de áudio (.ogg / .wav) e padroniza para o formato ideal para o whisper
    audio = AudioSegment.from_file(caminho_arquivo)
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)

    ''' Converte os bytes bruto em array NumPy float32 normalizado em ponto flutuante(-1.0 a 1.0) 
        evitando explosão de gradiente, portanto perda de sentido'''
    raw_data = audio.raw_data
    audio_np = (
        np.frombuffer(raw_data, dtype=np.int16).astype(np.float32) / 32768.0
    )

    # Transcreve com o Whisper
    resultado = modelo_whisper.transcribe(
        audio_np, language="pt", fp16=False  # fp16=False garante compatibilidade com CPU
    )

    # Retorna o texto limpo
    return resultado.get("text", "").strip()



@bot.message_handler(content_types=['voice', 'audio'])
def processar_audio(message):
    chat_id = message.chat.id
    temp_audio_path = f"temp_voice_{message.message_id}.ogg"

    try:
        bot.send_chat_action(chat_id, 'typing')

        # Download do áudio enviado no Telegram
        file_info = bot.get_file(message.voice.file_id if message.voice else message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open(temp_audio_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Transcrição via Whisper
        texto_transcrito = transcrever_audio_whisper(temp_audio_path)

        if not texto_transcrito:
            bot.send_message(chat_id, "⚠️ Não consegui entender o áudio.")
            return

        # Atribui o texto transcrito à mensagem
        message.text = texto_transcrito
        
        # Exibe a transcrição no terminal
        print(f"[Transcrição] Texto: {texto_transcrito}")

        processar_mensagem(message)  # Chama a função de processamento de mensagem com o texto transcrito 

        # Aqui você envia 'message' com o 'message.text' atualizado para a sua lógica de processamento
        # Exemplo: processar_mensagem_com_ia(message)

    except Exception as e:
        print(f"[Erro no Áudio] {e}")
        bot.send_message(chat_id, "❌ Erro ao processar o áudio")

    finally:
        # Exclusão do arquivo temporário
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

@bot.message_handler(func=lambda message: True)
def reply_hi(message):
  bot.send_message_draft(message.chat.id,20,'')
  print("Mensagem recebida!")

  # ADICIONADO: filtros extras são aplicados somente aos resultados atuais, não ao DataFrame original.
  estado = estados_pesquisa.get(message.chat.id)
  if estado and estado.get("aguardando_filtro"):
    estado["aguardando_filtro"] = False
    try:
      filtros_novos = bot_recepção.extrator(texto_usuario=message.text)
      # ADICIONADO: aplica cada critério ao conjunto já encontrado; por exemplo,
      # "3 quartos" significa exatamente três quartos, não até três.
      df_refinado = aplicar_filtros_adicionais(
        df_atual=estado["resultados"],
        tipos_de_filtro=filtros_novos.tipos_de_filtro,
        valores_desejados=filtros_novos.valor_desejado
      )
      # ADICIONADO: substitui a seleção atual pelo subconjunto refinado e reinicia a paginação.
      estado["resultados"] = df_refinado.copy()
      estado["proximo_indice"] = 0
      estado["filtros"].extend(filtros_novos.tipos_de_filtro)
      estado["valores_filtros"].update(filtros_novos.valor_desejado)
      bot_recepção.apresentar_lote(message.chat.id, estado, estado["precisa_de_localizacao"])
    except Exception as erro:
      # ADICIONADO: se a interpretação falhar, mantém os resultados e permite tentar novamente.
      print(f"Erro ao aplicar filtro adicional: {erro}")
      estado["aguardando_filtro"] = True
      bot.send_message(message.chat.id, "Não consegui identificar esse filtro com segurança. Pode reformular o critério que deseja acrescentar?")
    return
  
  # ADICIONADO: após Nova Pesquisa, a próxima mensagem inicia uma busca independente.
  if estado and estado.get("aguardando_nova_pesquisa"):
    estados_pesquisa.pop(message.chat.id, None)

  if not está_rodando:
    print("Inciando a o bot...")
    historico_conversa.append(message.text)
    #Usando a instância com a mensagem que o cliente mandar
    resultado_interação = processar_mensagem(message)
  else:
    print("Reiniciando o bot...")
    message.text = historico_conversa[-1] + ", e quero também com " + message.text
    historico_conversa.append(message.text)
    #Usando a instância com a mensagem que o cliente mandar
    resultado_interação = processar_mensagem(message)

bot.polling()
