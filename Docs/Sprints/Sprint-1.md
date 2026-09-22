# API 1º Semestre ADS - FATEC

# Imóveis SP - Chatbot Telegram

# Documentação - Sprint 1

<p align="center">
  <img src="../images/logo.png" alt="Logo do Projeto" width="200">
</p>

<h1 align="center">Ribbit</h1>

<p align="center">
  | <a href ="#desafio"> Desafio</a>  |
  <a href ="#us"> User Stories</a>  |   
  <a href ="#dor">DoR</a>  |
  <a href ="#dod">DoD</a>  |
</p>

> **Status do Projeto:** Em Desenvolvimento ⏳

## 🏅 Desafio <a id="desafio"></a>

**Implementar a infraestrutura base do Chatbot no Telegram focado em Imóveis (SP) e o sistema de busca essencial.** O objetivo principal desta entrega é permitir que o usuário realize consultas de imóveis disponíveis através de filtros básicos na interface do bot, além de estruturar os módulos iniciais para o consumo e exibição de notícias gerais sobre o mercado imobiliário e dados regionais (saúde pública, criminalidade e infraestrutura).

## 📋 User Stories <a id="us"></a>

| Ranking | Prioridade | User Story | Story Points | Sprint | Status |
| :------: | :--------: | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------: | :----: | :----: |
|     1    |    Alta    | Como comprador, gostaria de encontrar com facilidade os imóveis disponíveis do banco de dados com uma busca básica, para ter mais facilidade ao encontrar um imóvel de acordo com meus parâmetros.             |      20      |   1    |   0%   |
|     4    |    Alta    | Como comprador, gostaria de ter uma mini apresentação do imóvel, com as características dele, fotos e link da imobiliária.                                                                                                      |      14      |   1    |   0%   |
|     9    |    Alta    | Como cliente, gostaria de receber uma localização aproximada do endereço do imóvel. | 14 | 1 | 0% |

## 🏅 DoR - Definition of Ready <a id="dor"></a>

|             Critério             | Descrição                                                                                                            |
| :------------------------------: | -------------------------------------------------------------------------------------------------------------------- |
|       Clareza na Descrição       | A User Story está escrita no formato “Como [persona], quero [ação] para que [objetivo]”                              |
| Critérios de Aceitação Definidos | A história possui critérios objetivos que indicam o que é necessário para considerá-la concluída.                    |
|    Compreensão Compartilhada     | Toda a equipe (incluindo PO e devs) compreende o propósito da história.                                              |
|            Estimável             | A história foi pontuada no Planning Poker ou tem uma estimativa clara.                                               |
|       Documentos de Apoio        | Se necessário, mockups, CSV, fluxos ou modelos de dados estão anexados ou referenciados.                             |
|   Critérios técnicos acordados   | As necessidades do Telegram e das Funcionalidades locais foram claramente separadas (quando aplicável).              |

## 🏅 DoD - Definition of Done <a id="dod"></a>

|                 Critério                 | Descrição                                                                            |
| :--------------------------------------: | ------------------------------------------------------------------------------------ |
|           Criterio aceitacao             | Código revisado por pelo menos 2 devs e aprovado por maioria simples do Dev Team (sem bugs ou halucinacoes do LLM que fujam das ferramentas usadas)                 |
|             Codigo Testado               | Precisa funcionar em pelo menos dois computadores que não sejam da pessoa desenvolvendo o codigo                               |
|             Código revisado              | O código foi revisado por pelo menos um colega de equipe.                            |
|               Documentação               | O código está com sua função e expectativa atual de resultados coerente com a entrega, com perspectiva de melhorias quando necessário-- Item de backlog para futuras implementações da funcionalidade     está criado e atualizado         |
|  Integração com outras partes testadas   | As interfaces entre Telegram e ferramentas locais foram validadas.                   |
|             Validação do PO              | O Product Owner validou a entrega com base nos critérios definidos.                  |
|            Implementação                 | A funcionalidade está pronta para ser implementada no produto.                       |
