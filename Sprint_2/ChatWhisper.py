import os
import whisper
import telebot
import numpy as np
from pydub import AudioSegment

API_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "TOKEN_AQUI")
bot = telebot.TeleBot(API_TOKEN)


print("Carregando Whisper...")
modelo_whisper = whisper.load_model('small')
print("Whisper carregado!")


# ==============================================================================
# FUNÇÃO DE TRANSCRIÇÃO DE ÁUDIO
# ==============================================================================

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


# ==============================================================================
# HANDLER RECEBIMENTO DE ÁUDIO NO TELEGRAM
# ==============================================================================

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
        
        # Exibe a transcrição no chat do Telegram
        bot.send_message(chat_id, f"🎙️ *Texto Transcrito:* _\"{texto_transcrito}\"_", parse_mode="Markdown")

        # Aqui você envia 'message' com o 'message.text' atualizado para a sua lógica de processamento
        # Exemplo: processar_mensagem_com_ia(message)

    except Exception as e:
        print(f"[Erro no Áudio] {e}")
        bot.send_message(chat_id, f"❌ Erro ao processar o áudio: {str(e)}")

    finally:
        # Exclusão do arquivo temporário
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)



if __name__ == "__main__":
    bot.polling(non_stop=True)
