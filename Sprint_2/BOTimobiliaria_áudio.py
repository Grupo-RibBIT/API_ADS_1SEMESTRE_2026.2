def processar_mensagem(message):
   try:
      print(f"Mensagem incaminhada para o DSPy!!")
      print(f"Mensagem recebida: {message.text}")

      resultado_interação = bot_recepção(mensagem=message)

      print(f"DSPY terminou o processamento.!")

      resposta = getattr(resultado_interação, "final", None)

      if resposta:
          bot.send_message(message.chat.id, str(resposta))
      else:
          print("O DSPy não retornou o campo 'final'.")
          print(f"Erro: {resultado_interação}")
          bot.send_message(message.chat.id, "⚠️ Não consegui gerar uma resposta para o pedido.")

   except Exception as e:
        print(f"[Erro] {e}")
        bot.send_message(message.chat.id, f"❌ Erro ao processar a mensagem: {str(e)}")

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
        bot.send_message(chat_id, f"❌ Erro ao processar o áudio: {str(e)}")

    finally:
        # Exclusão do arquivo temporário
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

@bot.message_handler(func=lambda message: True)
def reply_hi(message):
  print("Mensagem recebida!")
  processar_mensagem(message)


bot.polling()
