# API 1º Semestre ADS - FATEC

# Imóveis SP - Chatbot Telegram

<p align="center">
  <img src="./Docs/images/logo.png" alt="Logo do Projeto" width="200">
</p>

<h1 align="center">Ribbit</h1>

<p align="center">
  <a href="#desafio">Desafio</a> | 
  <a href="#solucao">Solução</a> | 
  <a href="#backlog">Backlog do Produto</a> | 
  <a href="#sprint">Cronograma de Sprints</a> | 
  <a href="#tecnologias">Tecnologias</a> | 
  <a href="#manual">Manual de Instalação</a> | 
  <a href="#equipe">Equipe</a>
</p>

<br>

<p align="center">
> Status do Projeto:** Em Desenvolvimento ⏳
</p>

<p align="center">
 🏅 Desafio <a id="desafio"></a>

O desafio consiste em desenvolver um **chatbot para o Telegram integrado com uma Inteligência Artificial (IA) Local**, focado no mercado imobiliário de **São Paulo (SP)**. O bot deve consumir dados de uma base CSV pré-existente contendo informações detalhadas sobre casas e apartamentos à venda, incluindo valores, localidades e características específicas dos imóveis, permitindo uma interação inteligente, fluida e acessível tanto para compradores quanto para vendedores.
</p>

<p align="center">
 🏅 Solução <a id="solucao"></a>

A solução consiste em um assistente virtual interativo no Telegram que processa consultas em linguagem natural. Utilizando técnicas de IA para buscar informações na base de dados imobiliária, o chatbot ajuda compradores a encontrar o imóvel ideal através de buscas refinadas, comandos de voz e insights de localização. Para os vendedores, o sistema fornece dados analíticos sobre as preferências do mercado e alertas de lacunas de informação na base de dados, potencializando a especulação e a assertividade imobiliária na região de SP.
</p>
---

 📋 Backlog do Produto <a id="backlog"></a>

| Prioridade | User Story | Esforço (SP) | Sprint | Status |
| :--: | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------: | :----: | :----: |
| Alta | Como comprador, gostaria de encontrar com facilidade os imóveis disponíveis do banco de dados com uma busca básica, para ter mais facilidade ao encontrar um imóvel de acordo com meus parâmetros. | 20 | 1 | 0% |
| Alta | Como comprador, gostaria de ter prévias apresentações do imóvel para escolher um que esteja de acordo com as necessidades diárias como pontos de interesse próximos. | 36 | 3 | 0% |
| Alta | Como vendedor, gostaria de saber quais são os requisitos mais procurados pelos compradores no último mês ou semana (utilizando um contador de especificidades). | 60 | 3 | 0% |
| Média | Como vendedor ou comprador, gostaria de ter acesso a notícias recentes relacionadas à pesquisa no banco de dados para especulação imobiliária (saúde pública, pragas, criminalidade, infraestrutura, etc).  | 14 | 1 | 0% |
| Média | Como Comprador ou Vendedor, gostaria de um ID de usuário, para que minhas buscas sejam salvas e eu consiga continuar as minhas pesquisas. | 60 | 3 | 0% |
| Média | Como comprador, gostaria de me comunicar com o chatbot por áudio para ser acessível para um maior número de pessoas. | 65 | 2 | 0% |
| Baixa | Como vendedor, gostaria de ser informado quando a ia não tiver as informações necessárias para que eu possa acrescentar no banco de dados. (ex: piscina no imóvel, quadra, condomínio, etc) | 36 | 2 | 0% |
| Baixa | Como comprador, gostaria de ter um link aproximado do google maps para que possa ver a localização aproximada dos imóveis visualmente. | 45 | 2 | 0% |
| Baixa | Como cliente, gostaria de ser reconhecido se sou comprador ou vendedor para ter recomendações que melhor atendam  minhas necessidades. | 14 | 1 | 0% |

---
<p align="center">
 🏅 DoR - Definition of Ready <a id="dor"></a>

|             Critério             | Descrição                                                                                                            |
| :------------------------------: | -------------------------------------------------------------------------------------------------------------------- |
|       Clareza na Descrição       | A User Story está escrita no formato “Como [persona], quero [ação] para que [objetivo]”                              |
| Critérios de Aceitação Definidos | A história possui critérios objetivos que indicam o que é necessário para considerá-la concluída.                    |
|    Compreensão Compartilhada     | Toda a equipe (incluindo PO e devs) compreende o propósito da história.                                              |
|            Estimável             | A história foi pontuada no Planning Poker ou tem uma estimativa clara.                                               |
|       Documentos de Apoio        | Se necessário, mockups, CSV, fluxos ou modelos de dados estão anexados ou referenciados.                             |
|   Critérios técnicos acordados   | As necessidades do Telegram e das Funcionalidades locais foram claramente separadas (quando aplicável).              |
</p>

<p align="center">
 🏅 DoD - Definition of Done <a id="dod"></a>

|                 Critério                 | Descrição                                                                            |
| :--------------------------------------: | ------------------------------------------------------------------------------------ |
|           Criterio aceitacao             | Código revisado por pelo menos 2 devs e aprovado por maioria simples do Dev Team (sem bugs ou halucinacoes do LLM que fujam das ferramentas usadas)                 |
|             Codigo Testado               | Precisa funcionar em pelo menos dois computadores que não sejam da pessoa desenvolvendo o codigo                               |
|             Código revisado              | O código foi revisado por pelo menos um colega de equipe.                            |
|               Documentação               | O código está com sua função e expectativa atual de resultados coerente com a entrega, com perspectiva de melhorias quando necessário-- Item de backlog para futuras implementações da funcionalidade     está criado e atualizado         |
|  Integração com outras partes testadas   | As interfaces entre Telegram e ferramentas locais foram validadas.                   |
|             Validação do PO              | O Product Owner validou a entrega com base nos critérios definidos.                  |
|            Implementação                 | A funcionalidade está pronta para ser implementada no produto.                       |
</p>

---
 📅 Cronograma de Sprints <a id="sprint"></a>

| Sprint | Período | Documentação |
| :---------: | :------------: | :-----------------------------------------: |
| 📌 SPRINT 1 | 07/09 - 27/09 | [Sprint 1 Docs](./Docs/Sprints/Sprint-1.md) |
| 📌 SPRINT 2 | 05/10 - 25/10 | [Sprint 2 Docs](./Docs/Sprints/Sprint-2.md) |
| 📌 SPRINT 3 | 02/11 - 22/11 | [Sprint 3 Docs](./Docs/Sprints/Sprint-3.md) |

---
<p align="center">
 💻 Tecnologias <a id="tecnologias"></a>
</p>
<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"></a>
   <a href="https://github.com/"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
 <a href="https://www.atlassian.com/software/jira"><img src="https://img.shields.io/badge/Jira-0052CC?style=for-the-badge&logo=jira&logoColor=white"/></a>
 <a href="https://web.telegram.org/k/"><img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/></a>

</p>

---
<p align="center">
 📖 Manual de Instalação <a id="manual"></a>

#Manual em planejamento.

 🛠 Pré-requisitos

- Acesso a internet
</p>
  
---
<p align="center">
 🏃‍♂️ Como Executar o Projeto (Em Breve)

# Instruções de instalação e execução serão adicionadas conforme o desenvolvimento do ambiente.
</p>

---
<p align="center">
 🎓 Equipe <a id="equipe"></a>

<div align="center">
  <table>
    <tr>
      <th>Membro</th>
      <th>Função</th>
      <th>Github</th>
    </tr>
    <tr>
      <td>Arthur</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/ThurraVrd"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
    </tr>
    <tr>
      <td>Camila</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/camilabernardis"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
    </tr>
    <tr>
      <td>Guilherme</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/Jmcguicampos2024"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
    </tr>
    <tr>
      <td>José</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/JBJ3Dart"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
    </tr>
    <tr>
      <td>Larissa</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/larissaggodoisantos-spec"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
    </tr>
    <tr>
      <td>Miguel</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/m1guelsoares"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
    </tr>
    <tr>
      <td>Thais</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/ThaisPiresDosSantos"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
    </tr>
    <tr>
      <td>Ulisses</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/kikuchi-uli"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
    </tr>
    <tr>
      <td>Wilian</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/WilianFerraz"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
    </tr>
    <tr>
      <td>Vinícius</td>
      <td>Desenvolvedor</td>
      <td>-</td>
    </tr>
  </table>
</div>
</p>
