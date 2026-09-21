import dspy
from ddgs import DDGS
import telebot
import random

def salvar_no_historico(remetente: str, texto: str):
    """Adiciona a mensagem ao histórico e garante o limite máximo de 10 itens."""
    # Nesse append ele manda pro histórico
    historico_conversa.append(f"{remetente}: {texto}")
    
    # Ele salva até 10 intercaladas do bot e do usuario, e se passar ele tira as mais velhas.
    if len(historico_conversa) > 10:
        historico_conversa.pop(0) #Esse .pop(0) ele apaga a mensagem mais velha e sobe as outras de posição quando chegar a 11+

API_TOKEN = '8504434316:AAH7XLT3O8r4UJzvGeuCNBcKVsd-fPEAM3g'
bot = telebot.TeleBot(API_TOKEN)


lm = dspy.LM('ollama_chat/gemma4:e2b', api_base='http://localhost:11434', api_key='ignored')
dspy.configure(lm=lm)

suporte = dspy.ReAct("requisito_usuário -> resposta", tools=[salvar_no_historico])

# Aqui vai Salvar a conversa
historico_conversa = []


@bot.message_handler(func=lambda message: True)
def processar_historico(message):
    texto_usuario = message.text

    salvar_no_historico("Usuário", texto_usuario)

    resposta_do_bot = suporte(requisito_usuário=message.text)

    salvar_no_historico("Bot", resposta_do_bot)

    print("\n--- HISTÓRICO ATUALIZADO (MÁX 10 MENSAGENS) ---")
    for msg in historico_conversa:
        print(msg)
    print("----------------------------------------------\n")

    bot.reply_to(message,resposta_do_bot.reposta)

if __name__ == "__main__":
    print("🤖 Módulo de histórico ativo e escutando...")
    bot.polling(non_stop=True)