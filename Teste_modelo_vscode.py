import dspy
from ddgs import DDGS
import telebot
import random

infos_cruas ='2018-03-28T11:32:41Z;R$ 399.000;FALSO;36;Rua Major Diogo 39, Bela Vista - S�o Paulo/SP;1;1;1;22/11/2024'

list_fotos_apt = ["kamen-nikolov-fin","maxim-dorokhov","valmik-shah"]

def pesquisa_de_notícias(assunto_da_notícia:str):
  '''Procura por notícias de determinado assunto_da_notícia dentro da platafroma DuckDuckGo Search'''
  print("To vendo notícias...")
  notícias_achadas = DDGS().news(query=assunto_da_notícia,region="br-pt", max_results=5 )
  print(notícias_achadas)
  return notícias_achadas

API_TOKEN = '8504434316:AAH7XLT3O8r4UJzvGeuCNBcKVsd-fPEAM3g'
bot = telebot.TeleBot(API_TOKEN)


lm = dspy.LM('ollama_chat/gemma4:e2b', api_base='http://localhost:11434', api_key='ignored')
dspy.configure(lm=lm)

suporte = dspy.ReAct("requisito_usuário -> resposta", tools=[pesquisa_de_notícias])


def montar_mini_apresentação(p_fotos:str, num_banheiros:int) -> telebot.types.InputRichMessage:
  modelo_layout = f'''
  <tg-slideshow>

  ![](https://raw.githubusercontent.com/Grupo-RibBIT/arquivo-base/refs/heads/main/fotos_exemplo_apt/{p_fotos}-1.jpg)
  ![](https://raw.githubusercontent.com/Grupo-RibBIT/arquivo-base/refs/heads/main/fotos_exemplo_apt/{p_fotos}-2.jpg)
  ![](https://raw.githubusercontent.com/Grupo-RibBIT/arquivo-base/refs/heads/main/fotos_exemplo_apt/{p_fotos}-3.jpg)

  </tg-slidehow>

  #Apartamento ID563595
  ######Valor de Compra: ==R$ 500.000,00==

  | Infos do Apartamento | |
  |:---------|:--------:|
  | Área Útil| 65 m² |
  | Quartos | 2 (1 suíte) |
  | Banheiros | {num_banheiros} |
  | Vagas de Estacionamento | 3 |

  ###Destaques:
  - Tem piscina
  >**Para mais informações**: [Site da Imobiliária](https://github.com/Grupo-RibBIT)
  '''
  mensagem_rich = telebot.types.InputRichMessage(markdown=modelo_layout)
  return mensagem_rich

@bot.message_handler(func=lambda message: True)
def reply_hi(message):
  bot.send_message_draft(message.chat.id,20,'')
  print("Mensagem recebida!")
  #resultado = suporte(requisito_usuário = message.text)
  #pensamento = resultado.reasoning
  #bot.reply_to(message,pensamento)
  #bot.reply_to(message, resultado.resposta)
  foto_escolhida = random.sample(list_fotos_apt,1)
  print(foto_escolhida)
  bot.send_rich_message(message.chat.id,montar_mini_apresentação(foto_escolhida[0],50))

bot.polling()