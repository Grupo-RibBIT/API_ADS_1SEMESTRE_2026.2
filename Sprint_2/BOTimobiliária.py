# Biblioteca que o código está usando
import dspy
import telebot
import random
import re  # Biblioteca de Expressões Regulares (usada para extrair números de textos)
import pandas as pd  # Biblioteca para manipulação de dados e leitura do arquivo CSV
import time
from typing import Literal

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Bottelegram")

#Configuração do Bot/Telegram e do LLM

API_TOKEN = 'YOUR_TOKEN_HERE'
bot = telebot.TeleBot(API_TOKEN)

lm = dspy.LM('ollama_chat/qwen2.5-coder:7b', api_base='http://localhost:11434', api_key='ignored')
dspy.configure(lm=lm)

#Dados externos

list_fotos_apt = ["kamen-nikolov-fin","maxim-dorokhov","valmik-shah"]

path_csv = "/home/jbj/Área de trabalho/aula_jean/API_ADS_1SEMESTRE_2026.2/Sprint_1/apartamentos_sp_estruturado.csv"

TiposFiltro = Literal["preço_num","Área","Endereço","Quartos","Banheiros","Vagas_de_estacionamento"]

mini_csv ='''
created_date,Preço,below_price,Área,Endereço,Quartos,Banheiros,Vagas_de_estacionamento,extract_date
2018-05-24T15:02:18Z,R$ 2.000.000,FALSO,62,"Alameda Casa Branca 909, Jardim Paulista - São Paulo/SP",1,1,1,2024-11-22
'''

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
  '''Analisa o desejo_do_cliente extraído pelo Atendente e classifica com Bool (True ou False) se a mensagem possui as palavras apresentação e/ou localização e/ou um imóvel'''
  analisar_escopo:str = dspy.InputField()
  lista_de_ferramentas:list = dspy.InputField(desc="Lista de ferramentas usadas pelos sub-modulos")
  precisa_de_localizacao:bool = dspy.OutputField(desc="Define se o cliente mencionou/pediu localização de um imóvel, que precisará ser enviada")
  precisa_de_apresentacao:bool = dspy.OutputField(desc="Define se o cliente mencionou/pediu a apresentação ou mini-apresentação de um imóvel, que precisará ser enviada")
  precisa_de_busca_no_csv:bool = dspy.OutputField(desc="Define se o cliente mencionou/pediu um imóvel, uma rua, um bairro, ou uma informação sobre um imóvel, que precisará ser buscada no csv")


class ExtrairFiltros(dspy.Signature):
  """Extrai filtros de busca de imóveis a partir do pedido do usuário."""
  texto_usuario: str = dspy.InputField()
  tipos_de_filtro: list[TiposFiltro] = dspy.OutputField(desc="Lista com os tipos de filtragem/colunas do CSV,sendo 'Área' a área últil construida do apartamento")
  valor_desejado: dict[TiposFiltro,list] = dspy.OutputField(desc="Valores desejados do cliente, se tiver um só valor, a lista vai conter só uma variavel e se tiver mais de uma variável é um intevalo que engloba esses valores")


class FiltrosDoCSV(dspy.Signature):
  '''Acha apartamentos que se encaixam no requisitos do cliente dentro do csv'''
  df_bruto = dspy.InputField(desc="Dataframe completo dos apartamentos")
  tipos_de_filtro: list[TiposFiltro] = dspy.InputField(desc="Lista com os tipos de filtragem/colunas do CSV,sendo 'Área' a área últil construida do apartamento")
  valor_desejado: dict[TiposFiltro,list] = dspy.InputField(desc="Valores desejados do cliente, se tiver mais de uma variável é um intevalo que engloba esses valores")
  lista_apartamentos_str:list = dspy.OutputField(desc="Lista dos apartamentos achados pelo filtro em formato de sting")


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

  bot.send_message_draft(chat_id_telegram,20,'')

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

  print(modelo_layout)
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
    else:
      if len(valores_desejado_atual) >= 2:
          v_min, v_max = min(valores_desejado_atual[0], valores_desejado_atual[1]), max(
              valores_desejado_atual[0], valores_desejado_atual[1]
          )
          df = df[
              (df[tipo] >= v_min) & (df[tipo] <= v_max)
          ]
      else:
          df = df[df[tipo] <= valores_desejado_atual[0]]
  
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

#Criação do Modulo Geral

class BotImobiliária(dspy.Module):
  def __init__(self,dataframe):
    super().__init__()

    self.dataframe = dataframe

    #Definindo os sub-modulos

    self.gerenciador = dspy.ChainOfThought(EscolhasGerenciador)

    self.atendente = dspy.ChainOfThought(EscolhasAtendente)

    self.extrator = dspy.ChainOfThought(ExtrairFiltros)
    
    self.filtrador = dspy.ReAct(FiltrosDoCSV, tools=[filtrar_csv,transformar_dataframe_para_string])

    self.arquiteto = dspy.ChainOfThought(DescriçãoApartamento)

    self.apresentador = dspy.ReAct(CaracterísticasApresentação, tools=[montar_mini_apresentação_e_mandar_pelo_telegram])

    self.navegador = dspy.ReAct("endereço_apartamento, chat_id_telegram -> localização", tools=[enviar_localizacao_no_telegram], max_iters=3)

    self.finalizador = dspy.ReAct("resultado_do_pensamento -> resposta_final_cliente",tools=[])

  #A função foward diz como o modulo geral vai funcionar

  def forward(self, mensagem) -> dspy.Prediction:
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

        inicio = time.time()
        apartamentos_achados = filtrar_csv(tipo_de_filtragem=filtros_de_pesquisa.tipos_de_filtro,valores_desejados=filtros_de_pesquisa.valor_desejado,df_bruto=self.dataframe)
        fim = time.time()
        print(f"Apartamentos obtidos em {fim - inicio:.2f} segundos")
        print(apartamentos_achados)

        linhas = transformar_dataframe_para_string(apartamentos_achados)
        for n_linha in range(len(linhas)):
          if n_linha > 4:
            break
          linha_achada = linhas[n_linha]
          caracteristicas = self.arquiteto(linha_do_csv=linha_achada)
          print(caracteristicas)
          linha_de_pensamento += f'''
                #Caracterísca encontradas
                 {caracteristicas}

                  '''
          if escopo_do_pedido.precisa_de_apresentacao or escopo_do_pedido.precisa_de_localizacao:
            foto_escolhida = random.randint(0,2)
            slides = list_fotos_apt[foto_escolhida]
            apresentação = self.apresentador(
              fotos = slides, 
              banheiros = caracteristicas.banheiros, 
              quartos = caracteristicas.quartos, 
              área = caracteristicas.área, 
              valor = caracteristicas.valor, 
              estacionamento = caracteristicas.estacionamento, 
              chat_id_telegram = mensagem.chat.id)
            linha_de_pensamento += f'''
            ## Apresentação
            {apresentação}

              '''
        
            coordenadas = self.navegador(endereço_apartamento=caracteristicas.endereço_apartamento, chat_id_telegram=mensagem.chat.id)
            print(coordenadas)
            linha_de_pensamento += f'''
                    ## Coordenadas
                    {coordenadas}
            
                      '''

    print(linha_de_pensamento)

    final = self.finalizador(resultado_do_pensamento=linha_de_pensamento).resposta_final_cliente

    return dspy.Prediction(final)

#Criando uma instância do modulo geral
bot_recepção = BotImobiliária(dataframe=df)

@bot.message_handler(func=lambda message: True)
def reply_hi(message):
  bot.send_message_draft(message.chat.id,20,'')
  print("Mensagem recebida!")

  #Usando a instância com a mensagem que o cliente mandar
  resultado_interação = bot_recepção(mensagem=message)

bot.polling()