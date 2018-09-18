**Histórico de Revisão**

**Data** | **Versão** | **Descrição** | **Autor(es)**
---------|------------|---------------|---------------
18/08/2018| 1.0| Elaboração do modelo do termo de abertura do projeto | Gabriel Choptian
23/08/2018| 1.0.1| Revisão gramatical da versão 1.0 | Gabriel Choptian / Caio C.H. Nakai
05/09/2018| 1.0.2| Atualização dos tópicos 2, 3, 4 e 5 | Gabriel Choptian / Eduardo Yuzo Nakai
11/09/2018| 1.0.3| Correção e adição de novas informações | Caio Nakai / Eduardo Nakai

## Sumário
 
1. [Objetivos deste documento](#1-Objetivos-deste-documento)
2. [Descrição do Projeto](#2-descri%C3%A7%C3%A3o-do-projeto)
3. [Justificativa](#3-justificativa)
4. [Objetivo do Projeto (SMART)](#4-objetivo-do-projeto-smart)
5. [Produto do Projeto](#5-produto-do-projeto)
6. [Restrições](#6-restrições)
7. [Riscos Iniciais](#7-riscos-iniciais)
8. [Cronograma e Marcos](#8-cronograma-e-marcos)
9. [Custo Estimado do Projeto](#9-custo-estimado-do-projeto)    
  9.1. [Recursos Humanos](#91-recursos-humanos)    
  9.2. [Equipamentos e Serviços](#92-equipamentos-e-serviços)    
  9.3. [Custo Total](#93-custo-total)    
10. [Stakeholders (Partes interessadas)](#10-stakeholders-partes-interessadas)    
  10.1. [Cliente](#101-cliente)    
  10.2. [Equipe de Gerência](#102-equipe-de-gerencia)    
  10.3. [Equipe de Desenvolvimento](#103-equipe-de-desenvolvimento)    
11. [Referência Bibliográfica](#11-refer%C3%AAncia-bibliogr%C3%A1fica)

# 1. Objetivos deste documento
<p align = "justify">Autorizar o início do projeto, atribuir principais responsáveis e documentar requisitos iniciais, principais entregas, premissas e restrições.</p>

# 2. Descrição do Projeto

<p align = "justify"> 
  Com base em dados de ocorrências das plantas, os quais serão correlacionados a variáveis ambientais para a predição da área de distribuição geográfica das espécies no presente e no futuro, pretendemos
  identificar os seguintes fatores: 
  
  - Áreas de maior diversidade;
  - Famílias e táxons amplamente distribuídas;
  - Famílias e táxons com áreas restritas de ocorrência. 
</p>

# 3. Justificativa

<p align = "justify">  O projeto entra no contexto da elaboração de um sistema para aplicação de pesquisas em ecologia de ambientes aquáticos com a finalidade de investigar padrões biogeográficos de macrófitas aquáticas na América do Sul.</p>

# 4. Objetivo do Projeto

<p align = "justify">
  O objetivo deste projeto envolve a elaboração de um sistema capaz de: 

  1) Validar os nomes das espécies de macrófitas em banco de dados disponíveis online, trazendo também informações relacionadas à Taxonomia, Ecologia e Biologia. Com relação às bases de dados disponíveis online: SpeciesLink, GBIF, The Plant List, , 
  2) Congregar informações de registros de ocorrências dessas espécies de macrófitas no continente da seguinte forma. Correção de erros através da comparação entre os dados de diferentes bases; indicação de padrões e tendências considerando as bacias hidrográficas Sul-Americanas.
</p>

# 5. Produto do Projeto
A. **Escopo**
  - Validar o nome da espécies, fornecendo o nome atualmente aceito e autor.
  - Extração de dados categóricos da espécie apartir do nome da espécie 
  - Listar os dados de ocorrência de cada espécie a partir das plataformas SpeciesLink e GBIF. 
  - Executar processo triagem dos dados e correção de inconsistências.
  - Visualização dos dados correlacionados.

B. **Não Escopo**
- Não serão coletados dados que não estejam nas bases especificadas.

C. **Requisitos de alto nível**

Os requisitos de maior prioridade ao cliente são:
- Sistema funcionando corretamente: extração, correção e correlação das informações obtidas, de forma consistente e correta.

C. **Requisitos do Sistema**
  - [RF1] O sistema deve aceitar e processar os dados de espécies num formato específico.
  - [RF2] O sistema deve extrair dados de espécies de bases de dados online.
	  - Flora do Brasil
    - The Plant List
  - [RF3] O sistema deve extrair dados de ocorrência na América do Sul de espécies de bases de dados online.
	  - SpeciesLink.
	  - GBIF.
  - [RF4] O sistema deve corrigir os dados de espécies de entrada com base nos dados coletados online [RF2]: nomes duplicados, errados.
  - [RF5] O sistema deve corrigir os dados coletados online [RF3]: nomes errados, duplicados.
  - [RF6] O sistema deve relacionar os dados de ocorrências das espécies no Brasil com base nos dados obtidos de [RF2], [RF4].
  - [RF7] O sistema deve gerar uma tabela com as seguintes informações: data, autor, nome de espécie válida, coordenadas, país.

# 6. Restrições

As restrições do projeto são:
- O projeto deverá ser concluído até o final da disciplina 29/11/2018.

# 7. Riscos Iniciais

<p align = "justify"> Os principais riscos do projeto envolvem a equipe e a tecnologia a ser utilizada. Esses riscos exigem um plano de ação para se obter o sucesso do projeto, que são: </p>

**Riscos** | **Plano de Ação** 
-----------|------------|
Complicações na extração dos dados | Estudar tecnologias necessárias para extração dos dados
Correção dos dados | Estudar técnicas para correção dos dados
Cronograma do projeto | Modificar a documentação para refletir as mudanças necessárias

# 8. Cronograma e Marcos

<p align = "justify"> O cronograma do projeto se dá início ao semestre letivo da disciplina Engenharia de software 2, de maneira que teve seu marco inicial no dia 15/08/2018 e a data de finalização dia 29/11/2018. Entre essas datas acontecerão três entregas parciais: </p>

 **Pontos de Controles**     | **Data**          |  **Resumo** 
-----------------------------|-------------------|-----------
Release 01                   | 21/09/2018 | Gerenciamento do projeto e estudo das tecnologias
Release 02                   | 05/10/2018 | Extração dos dados
Release 03                   | 19/11/2018 | Visualização e correlação dos dados

# 9. Custo estimado do projeto
## 9.1. Recursos Humanos

<p align = "justify"> O custo existente no projeto relativo aos recursos humanos refere-se ao valor gasto com toda equipe presente em seu desenvolvimento e gestão.</p>

<p align = "justify"> A equipe conta com 3 membros. O valor custo médio de um membro da equipe, o qual será medido em hora, supondo que cada participante reserve em média 5h por semana, extra aula para realizar as atividades do projeto, teremos o custo:</p>

|            | **Quantidade de Pessoas** | **Horas Por Semana** | **Semanas** | Preço Por Pessoa | Custo Final     |
|---|:---:|:---:|:---:|:---:|-----------------|
Membro |   3    |          5h          |      15      |      -    |   225h  |

## 9.2. Equipamentos e Serviços

<p align = "justify"> O custo existente no projeto relativo aos equipamentos e serviços refere-se a todo e qualquer equipamento ou serviço utilizado para o desenvolvimento do mesmo. </p>

<p align = "justify"> Fora estimado que cada membro irá utilizar um Notebook com todas as ferramentas necessárias para o desenvolvimento do projeto.</p>

<!--<p align = "justify"> Há também o custo mensal de energia elétrica gasta. Para o seu cálculo foi considerado que o preço do kWh seria de aproximadamente R$ 0,589. Como cada Notebook tem potência em torno de 80W e cada integrante irá trabalhar por 5 horas semanais, o gasto individual com energia elétrica mensal fica da seguinte forma:</p>

(1 Notebook * 80W *  5 horas/semana * 14 semanas) / 1000 = 0,056 kWh/mês
 
4,16 kWh/mês * 0,589 = R$ 3,29

Os custos totais podem ser observados na tabela abaixo:

 **Descrição**| **Preço Unitários** | **Quantidade** | **Preço Final** |  
--------------|---------------------|----------------|-----------------|
Notebook Dell | -  |          3 |    - |      
Banda Larga        | -     | 3 por 4 meses | -  |      
Energia Elétrica        | R$ 2,45024   | 3 por 4 meses | R$ 39,58    | 
Custo Estimado          |              |                | R$ 39,58 |
-->
<!--## 9.3. Custo Total

<p align = "justify"> O custo total é representado pela soma dos custos de Recursos Humanos e o custo total dos equipamentos e serviços: </p>

 **Custo de Recursos Humanos**| **Custo de Equipamentos e Serviços** | **Custo Total Estimado** |  
------------------------------|--------------------------------------|--------------------------|
219h                  |              R$ 39,58            |       219h e R$ 39,58       |
-->
# 10. Stakeholders (Partes interessadas)

## 10.1. Clientes

| Nome | Ocupação | E-mail |
| --- | --- | --- |
|Tania | Aluna |taniacrivelari@hotmail.com |
|Karina | Professora |  karina.fidanza@gmail.com |
|Dayani Bailly | Aluna de pós-doutorado | dayanibailly@gmail.com |

## 10.2.  Equipe de Gerência

<p align = "justify"> Os alunos da disciplina de engenharia de software têm o objetivo de planejar, controlar e tomar decisões importantes para que o projeto seja concluído com êxito. </p>

| Nome | E-mail |   GitHub |  
|---|---|--- |
|Caio Cesar Hideo Nakai|caionakai2015@gmail.com|[@caionakai](https://github.com/caionakai)|  
|Eduardo Yuzo Nakai|yuzonakai@gmail.com|[@tabsnospaces](https://github.com/tabsnospaces)|  
|Gabriel Choptian|choptian@alunos.utfpr.edu.br|[@ltdagabriel](https://github.com/ltdagabriel)|  

## 10.3. Equipe de Desenvolvimento

<p align = "justify"> A equipe de desenvolvimento são os membros da equipe de gerência, considerando que o objetivo do projeto é a aprendizagem de gerência de projetos.  </p>

# 11. Referência Bibliográfica

* PMI. *Um guia do conhecimento em gerenciamento de projetos. * Guia PMBOK® 5a. ed. - EUA: Project Management Institute, 2013

* **¹** MONTES, Eduardo. **TERMO DE ABERTURA DO PROJETO**. Disponível em <[https://escritoriodeprojetos.com.br/termo-de-abertura-do-projeto](https://escritoriodeprojetos.com.br/termo-de-abertura-do-projeto)> Acesso em 18/08/2018
