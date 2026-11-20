# 🏡 My Contribution to the Real Estate Telegram Bot

*[Leia em Português](#-minha-contribuição-para-o-telebot-imobiliário)*

In this part of the project, I focused on improving the communication between the Telegram bot and its users while requests were being processed.

Previously, users could experience periods without visible feedback while the bot performed operations such as interpreting requests, filtering properties, and generating responses.

My goal was to make this interaction clearer by implementing intermediate messages using Telegram's `send_message_draft_` command.

---

## 💬 Intermediate Messages During Processing

I implemented intermediate message functionality using `send_message_draft_` to provide feedback while the bot processes user requests.

Instead of relying exclusively on the final response, the bot can display a draft message during processing, indicating that the request is being handled.

This improves the interaction by reducing the impression that the bot has stopped responding.

The implementation focuses on:

- **Processing feedback:** displaying an intermediate draft while the bot handles a request.
- **Telegram integration:** using the `send_message_draft_` command to interact with Telegram's draft messaging functionality.
- **User experience:** providing visual feedback during operations that may take some time.
- **Message handling:** using drafts instead of relying on repeatedly editing already-sent messages.

---

## 🔧 Integration with the Existing Bot

I integrated the intermediate messaging functionality into the existing bot workflow, preserving its main operations.

The implementation was designed to work alongside the existing features, including:

- Property searches and CSV filtering.
- Property presentations.
- AI-powered response generation through DSPy.
- Audio message processing using Whisper.

The intention was to improve communication without changing the existing search and property selection logic.

---

## 📁 Files Involved

| File | Changes |
| --- | --- |
| `BOTimobiliaria.py` | Integration of intermediate draft messages into the Telegram bot's processing workflow. |

---

## ✅ Final Result

With this implementation, the bot provides users with intermediate feedback while processing their requests.

My contribution focused on improving the communication between the bot and its users, making the waiting period more transparent and the overall interaction more responsive.

---

# 🏡 Minha contribuição para o Telebot Imobiliário

*[Read in English](#-my-contribution-to-the-real-estate-telegram-bot)*

Nesta parte do projeto, concentrei meu trabalho em melhorar a comunicação entre o bot do Telegram e seus usuários durante o processamento das solicitações.

Anteriormente, o usuário podia passar por períodos sem receber um retorno visível enquanto o bot executava operações como interpretação de mensagens, filtragem de imóveis e geração de respostas.

Meu objetivo foi tornar essa interação mais clara, implementando mensagens intermediárias por meio do comando `send_message_draft_`.

---

## 💬 Mensagens intermediárias durante o processamento

Implementei a funcionalidade de mensagens intermediárias utilizando `send_message_draft_`, permitindo fornecer um retorno visual enquanto o bot processa as solicitações dos usuários.

Em vez de depender exclusivamente da resposta final, o bot pode apresentar uma mensagem em formato de rascunho durante o processamento, indicando que a solicitação está sendo atendida.

Essa implementação melhora a interação, reduzindo a impressão de que o bot parou de responder.

Os principais pontos dessa implementação são:

- **Retorno durante o processamento:** apresentação de um rascunho enquanto o bot executa uma solicitação.
- **Integração com o Telegram:** utilização do comando `send_message_draft_` para trabalhar com a funcionalidade de mensagens em rascunho.
- **Experiência do usuário:** fornecimento de um retorno visual durante operações que podem levar algum tempo.
- **Gerenciamento de mensagens:** utilização de rascunhos em vez de depender de várias edições de mensagens já enviadas.

---

## 🔧 Integração com o bot existente

Integrei a funcionalidade de mensagens intermediárias ao fluxo de funcionamento do bot, preservando suas principais operações.

A implementação foi desenvolvida para trabalhar em conjunto com funcionalidades que já existiam no projeto, como:

- Pesquisas de imóveis e filtragem do CSV.
- Apresentação dos apartamentos.
- Geração de respostas utilizando IA por meio do DSPy.
- Processamento de mensagens de áudio com Whisper.

A intenção foi melhorar a comunicação sem alterar a lógica existente de pesquisa e seleção de imóveis.

---

## 📁 Arquivos envolvidos

| Arquivo | Alterações realizadas |
| --- | --- |
| `BOTimobiliaria.py` | Integração das mensagens intermediárias em formato de rascunho ao fluxo de processamento do bot no Telegram. |

---

## ✅ Resultado da implementação

Com essa implementação, o bot passa a fornecer um retorno intermediário ao usuário enquanto processa suas solicitações.

Minha contribuição foi melhorar a comunicação entre o bot e seus usuários, tornando o tempo de espera mais transparente e a interação mais responsiva.
