# API 1º Semestre ADS - FATEC

> Status do Projeto: Concluído ✅

# Imóveis SP - Chatbot Telegram

<p align="center">
  <img src="./Docs/images/logo.png" alt="Logo do Projeto" width="200">
</p>

<div align="center">
  
# Ribbit 

| <a href="#desafio">Desafio</a> | <a href="#solucao">Solução</a> | <a href="#backlog">Backlog do Produto</a> | <a href="#sprint">Cronograma de Sprints</a> | <a href="#tecnologias">Tecnologias</a> | 
<a href="#manual">Manual de Instalação</a> | <a href="#equipe">Equipe</a>

</div>

<div align="center">
  
## 🎯Desafio <a id="desafio"></a>

</div>

O desafio consiste em desenvolver uma solução inteligente e acessível que facilite a busca por imóveis no amplo mercado imobiliário da cidade de São Paulo. Através de uma base CSV pré-existente contendo informações detalhadas sobre apartamentos à venda - **incluindo valores, localidades, características específicas e informações das imobiliárias** - o sistema deve proporcionar consultas rápidas e personalizadas, permitindo que compradores encontrem imóveis de acordo com suas preferências. Além disso, o desafio contempla recursos de acessibilidade, análise de tendências do mercado, informações relevantes sobre as regiões e persistência de dados, possibilitando a continuidade das pesquisas e a conexão entre compradores e corretores para dar início ao processo de aquisição.

<div align="center">

## 🏅Solução <a id="solucao"></a>

</div>

A solução consiste em um **chatbot para o Telegram integrado com uma Inteligência Artificial (IA) Local**, capaz de realizar buscas imobiliárias personalizadas através de mensagens de texto e comandos de voz. Utilizando técnicas de processamento de dados e IA, o chatbot apresenta imóveis com **características detalhadas, fotografias, links das imobiliárias e localização aproximada**, proporcionando uma experiência de pesquisa prática e intuitiva. O sistema também oferece análises das preferências dos usuários, identificando tendências do mercado imobiliário, além de fornecer notícias recentes sobre as regiões pesquisadas. Para garantir uma experiência contínua, cada comprador possui um identificador único, permitindo armazenar seu histórico e retomar pesquisas anteriores. Por fim, o chatbot possibilita a seleção de imóveis de interesse e o encaminhamento a um corretor, facilitando o agendamento de visitas e o início do processo de compra.

<div align="center">
  
 ## Backlog do Produto <a id="backlog"></a>

</div>

| Ranking | Prioridade | User Story | Esforço (SP) | Sprint | Status |
| :-----: | :--------: | :---: | :----------: | :----: | :----: |
| 1 | Alta | Como comprador, gostaria de encontrar com facilidade os imóveis disponíveis na base de dados com uma busca básica, para ter mais facilidade ao encontrar um imóvel de acordo com meus parâmetros. | 20 | 1 | 100% |
| 2 | Alta | Como comprador, gostaria de ter uma mini apresentação do imóvel, com as características dele, fotos e link da imobiliária. | 14 | 1 | 100% |
| 3 | Alta | Como cliente, gostaria de receber uma localização aproximada do endereço do imóvel. | 14 | 1 | 100% |
| 4 | Média | Como comprador, gostaria de me comunicar com o chatbot por áudio para ser acessível para um maior número de pessoas. | 40 | 2 | 100% |
| 5 | Média | Como cliente, gostaria de saber quais são os requisitos mais procurados com base no histórico de pesquisas para saber as tendências do mercado atual. | 40 | 2 | 100% |
| 6 | Média | Como cliente, gostaria de ter acesso a notícias positivas recentes relacionadas à região do imóvel para ter mais argumentos de venda. | 20 | 2 | 100% |
| 7 | Baixa | Como Comprador, gostaria de um ID de usuário, para que minhas buscas sejam salvas e eu consiga continuar as minhas pesquisas. | 30 | 3 | 100% |
| 8 | Baixa | Como comprador, gostaria de escolher um imóvel e ser encaminhado a um corretor para finalizar minha pesquisa e dar inicio a compra/visita do imóvel | 20 | 3 | 100% |


<div align="center">
  
## DoR - Definition of Ready <a id="dor"></a>

</div>

|             Critério             | Descrição                                                                                                            |
| :------------------------------: | -------------------------------------------------------------------------------------------------------------------- |
|       Clareza na Descrição       | A User Story está escrita no formato “Como [persona], quero [ação] para que [objetivo]”                              |
| Critérios de Aceitação Definidos | A história possui critérios objetivos que indicam o que é necessário para considerá-la concluída.                    |
|    Compreensão Compartilhada     | Toda a equipe (incluindo PO e devs) compreende o propósito da história.                                              |
|            Estimável             | A história foi pontuada no Planning Poker ou tem uma estimativa clara.                                               |
|       Documentos de Apoio        | Se necessário, mockups, CSV, fluxos ou modelos de dados estão anexados ou referenciados.                             |
|   Critérios técnicos acordados   | As necessidades do Telegram e das Funcionalidades locais foram claramente separadas (quando aplicável).              |


<div align="center">
  
## DoD - Definition of Done <a id="dod"></a>

</div>

|                 Critério                 | Descrição                                                                            |
| :--------------------------------------: | ------------------------------------------------------------------------------------ |
|           Criterio aceitacao             | Código revisado por pelo menos 2 devs e aprovado por maioria simples do Dev Team (sem bugs ou halucinacoes do LLM que fujam das ferramentas usadas)                 |
|             Codigo Testado               | Precisa funcionar em pelo menos dois computadores que não sejam da pessoa desenvolvendo o codigo                               |
|             Código revisado              | O código foi revisado por pelo menos um colega de equipe.                            |
|               Documentação               | O código está com sua função e expectativa atual de resultados coerente com a entrega, com perspectiva de melhorias quando necessário-- Item de backlog para futuras implementações da funcionalidade     está criado e atualizado         |
|  Integração com outras partes testadas   | As interfaces entre Telegram e ferramentas locais foram validadas.                   |
|             Validação do PO              | O Product Owner validou a entrega com base nos critérios definidos.                  |
|            Implementação                 | A funcionalidade está pronta para ser implementada no produto.                       |

<div align="center">
  
## Cronograma de Sprints <a id="sprint"></a>

| Sprint | Período | Documentação | Link do Vídeo |
| :---------: | :------------: | :---: | :---: |
| 📌 SPRINT 1 | 07/09 - 27/09 | [Sprint 1 Docs](./Docs/Sprints/Sprint-1.md) | [Vídeo no Youtube](https://youtu.be/Ei-zJ9vX5ko)|
| 📌 SPRINT 2 | 05/10 - 25/10 | [Sprint 2 Docs](./Docs/Sprints/Sprint-2.md) | [Vídeo no Youtube](https://www.youtube.com/watch?v=XQPT6sW2TAQ) |
| 📌 SPRINT 3 | 02/11 - 22/11 | [Sprint 3 Docs](./Docs/Sprints/Sprint-3.md) | - | [Vídeo no Youtube](https://youtu.be/gbQfOIBRf9s?si=tEqogkno-HbNpaG9)

</div>

<div align="center">
  
## Tecnologias <a id="tecnologias"></a>

</div>

<div align="center">
  
 <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"></a>
 <a href="https://github.com/"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
 <a href="https://www.atlassian.com/software/jira"><img src="https://img.shields.io/badge/Jira-0052CC?style=for-the-badge&logo=jira&logoColor=white"/></a>
 <a href="https://web.telegram.org/k/"><img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/></a>
 <a href="https://www.json.org"><img src="https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white"/></a>
 <a href="https://openai.com/pt-BR/index/whisper/"><img src="https://img.shields.io/badge/Whisper-412991?style=for-the-badge&logo=openai&logoColor=white"/></a>
 <a href="https://www.openstreetmap.org/#map=5/-15.13/-53.19"><img src="https://img.shields.io/badge/OpenStreetMap-7EBC6F?style=for-the-badge&logo=openstreetmap&logoColor=white"/></a>
 <a href="https://geopy.readthedocs.io/en/stable/"><img src="https://img.shields.io/badge/GeoPy-4285F4?style=for-the-badge&logo=python&logoColor=white"/></a>
 <a href="https://pypi.org/project/RapidFuzz/"><img src="https://img.shields.io/badge/RapidFuzz-6A5ACD?style=for-the-badge&logo=python&logoColor=white"/></a>
 

</div>

<div>


<div align="center">

## 📖 Manual de Instalação <a id="manual"></a>

</div>

### 🛠 Pré-requisitos

Para executar o projeto localmente, é necessário:

- Acesso à internet.
- [Python](https://www.python.org/downloads/) instalado.
- [Telegram](https://telegram.org/) instalado ou acesso ao Telegram Web.
- [Ollama](https://ollama.com/download) instalado.
- [FFmpeg](https://ffmpeg.org/download.html) instalado para processamento de áudio.
- Arquivo CSV contendo os dados dos imóveis.

**Observação:** Durante a instalação do Python no Windows, habilite a opção `Add Python to PATH`. O FFmpeg também deve estar configurado no PATH do sistema.

<div align="center">

## 🚀 Como Executar o Projeto

</div>

### 1. Baixar o Repositório

Clone o repositório do GitHub ou baixe o projeto em formato ZIP e extraia os arquivos.

Abra o terminal na pasta do projeto.

### 2. Instalar as Dependências

Com o Python instalado, execute o seguinte comando no terminal:

```bash
python -m pip install -r requirements.txt
```

Esse comando instalará automaticamente as bibliotecas Python necessárias para o funcionamento do chatbot.

### 3. Configurar a Inteligência Artificial Local

Baixe e instale o [Ollama](https://ollama.com/download).

Após a instalação, abra o terminal e execute:

```bash
ollama pull qwen2.5-coder:7b
```

Esse comando realizará o download do modelo **Qwen 2.5 Coder 7B**, utilizado pelo chatbot para processamento de linguagem natural.

O Ollama deverá permanecer em execução durante a utilização do bot.

### 4. Criar um Bot no Telegram

1. Abra o Telegram ou [Telegram Web](https://web.telegram.org/).
2. Pesquise por **@BotFather**.
3. Inicie uma conversa e envie o comando `/newbot`.
4. Escolha um nome e um nome de usuário para o bot.
5. Copie o token de autenticação fornecido pelo BotFather.

No código Python do projeto, localize o campo:

```python
"YOUR TOKEN"
```

Substitua pelo token gerado pelo BotFather.

**Importante:** Nunca compartilhe ou publique seu token de autenticação no GitHub.

### 5. Configurar a Base de Dados

O chatbot utiliza uma base de dados imobiliária em formato CSV, contendo informações sobre os apartamentos disponíveis.

No código Python, localize o campo:

```python
"YOUR CSV PATH"
```

Substitua pelo caminho do arquivo CSV no seu computador.

**Atenção:** O arquivo CSV deve respeitar a estrutura e os parâmetros de dados utilizados pelo chatbot, incluindo os nomes das colunas esperadas pelo sistema.

### 6. Configurar o FFmpeg

Baixe o [FFmpeg](https://ffmpeg.org/download.html) e configure sua pasta `bin` no PATH do Windows.

Para verificar a instalação, execute:

```bash
ffmpeg -version
```

O FFmpeg é necessário para o processamento das mensagens de áudio recebidas pelo chatbot.

### 7. Executar o Chatbot

Com todas as dependências instaladas e configurações realizadas, abra o terminal na pasta do projeto e execute:

```bash
python NOME_DO_ARQUIVO.py
```

Substitua `NOME_DO_ARQUIVO.py` pelo nome do arquivo principal do chatbot.

Após a inicialização, abra o Telegram, encontre o bot criado e envie:

```text
/start
```

O chatbot estará pronto para receber consultas imobiliárias.

### 8. Utilizar o Bot Imobiliário

Também é possível acessar o chatbot desenvolvido originalmente através do link:

**[Bot Imobiliário no Telegram](https://t.me/Niemeyer_bot)**

A disponibilidade do bot depende de sua execução no ambiente em que está hospedado.

<div align="center">
  
## 🎓 Equipe <a id="equipe"></a>

<div align="center">
  <table>
    <tr>
      <th>Membro</th>
      <th>Função</th>
      <th>Github</th>
      <th>LinkedIn</th>
    </tr>
    <tr>
      <td>Camila</td>
      <td>Product Owner</td>
      <td><a href="https://github.com/camilabernardis"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
      <td><a href="https://www.linkedin.com/in/camila-bernardi-ti-"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
    </tr>
    <tr>
      <td>José</td>
      <td>Scrum Master</td>
      <td><a href="https://github.com/JBJ3Dart"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
      <td><a href="https://www.linkedin.com/in/jjuliatti"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
    </tr>
    <tr>
      <td>Arthur</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/ThurraVrd"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
      <td><a href="https://www.linkedin.com/in/arthurvrd1/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
    </tr>
    <tr>
      <td>Guilherme</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/Jmcguicampos2024"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
      <td><a href="https://www.linkedin.com/in/guilherme-baleeiro-gonçalves-de-campos-070aa9433?utm_source=share_via&utm_content=profile&utm_medium=member_android"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
    </tr>
    <tr>
      <td>Larissa</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/larissaggodoisantos-spec"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
      <td><a href="https://www.linkedin.com/in/larissa-godoi-95682b306/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
    </tr>
    <tr>
      <td>Miguel</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/m1guelsoares"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
      <td><a href="https://www.linkedin.com/in/mige3e3l-/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
    </tr>
    <tr>
      <td>Thais</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/ThaisPiresDosSantos"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
      <td><a href="https://www.linkedin.com/in/thais-pires-dos-santos?utm_source=share_via&utm_content=profile&utm_medium=member_android"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
    </tr>
    <tr>
      <td>Ulisses</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/kikuchi-uli"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
      <td><a href="https://linkedin.com/in/ulisses-kikuchi"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
    </tr>
    <tr>
      <td>Wilian</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/WilianFerraz"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
      <td><a href="https://www.linkedin.com/in/wilian-ferraz-mancilha-587a6619b?utm_source=share_via&utm_content=profile&utm_medium=member_android"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
    </tr>
    <tr>
      <td>Vinícius</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/viniconst85"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
      <td><a href="https://www.linkedin.com/in/vinicius-constantino-b3312a1a7"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
    </tr>
  </table>
</div>
</p>
