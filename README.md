## Classificação de Macrófitas
Com base em dados de ocorrência dessas plantas, os quais serão correlacionados à varáveis ambientais para a predição da área de distribuição geográfica da espécies no presente e no futuro, pretendemos identificar os seguintes fatores: 
  
  - Áreas de maior diversidade;
  - Famílias e táxons amplamente distribuídas;
  - Famílias e táxons com áreas restritas de ocorrência. 

Desta forma, o produto pretendido é definido por um sistema capaz de: 
  
  1) Validar os nomes das espécies de macrófitas em banco de dados disponíveis online (Specieslink e GBIF), trazendo também informações relacionadas à:
      - Taxonomia;
      - Ecologia;
      - Biologia.
  2) Congregar informações de registros de ocorrências dessas espécies de macrófitas no continente da seguinte forma:
      - Correção de erros;
      - Indicação de padrões e tendências considerando as bacias hidrográficas Sul-Americanas. 
## Requerimentos e como inicializar
 - Instalar [Python 3](https://www.python.org/downloads/)
 - Instalar [Pyinstaller](https://sourceforge.net/projects/pywin32/files/)
 - clonar ou baixar o projeto zipado
 - `git clone https://github.com/ltdagabriel/Database-Macrophytes.git`
 - `cd Database-Macrophytes`
 - `pip install -r scripts/requeriments.txt`
 - `pyinstaller "scripts/Extração das macrófitas.py"`
 - `copy "scripts/dict_final.txt" "scripts/dist/Extração das macrófitas/"`
 - `"scripts/dist/Extração das macrófitas/Extração das macrófitas.exe"`
 Executar
 - `"scripts/dist/Extração das macrófitas/Extração das macrófitas.exe"`

## Projeto compilado para arquitetura Windows 32
- Google DRIVE: [Extração das macrófitas.zip](https://drive.google.com/open?id=1XQ3fnZDMxEqzEO-Tt_RQwQ8-ErOVf1P0)

## Relação de Tempo
| Release | Tarefa                             | Tempo estimado | Tempo real    | Quem fez               |
|---------|------------------------------------|----------------|---------------|------------------------|
| 1       | Assinatura TAP                     |                | 6 horas       | Caio, Eduardo, Gabriel |
| 1       | Plano de Tempo                     |                | 6 horas       | Caio, Eduardo, Gabriel |
| 1       | Plano de Escopo                    |                | 4 horas       | Caio, Eduardo          |
| 1       | Termo de Abertura                  |                | 4 horas       | Caio, Eduardo, Gabriel |
| 1       | Manipulação dos dados de entrada   |                | 0.17 hora    | Gabriel                |
| 2       | [excluído]Correção dos dados: GBIF           | N/A  | N/A | N/A     |
| 2       | Extração dos dados:The Plant List  | 11 horas       | 4 horas       | Gabriel, Eduardo       |
| 2       | Extração dos dados:Splink          | 15 horas       | 20 horas      | Gabriel, Eduardo       |
| 2       | Extração dos dados:GBIF            | 7 horas        | 4 horas       | Gabriel, Caio          |
| 2       | Extração dos dados:Flora do Brasil | 7 horas             | 8 horas            | Eduardo      |
| 3       | Estudo de técnicas para correção dos dados | 7 horas | 3 horas | Caio, Eduardo, Gabriel |
| 3       | Gerar tabela de saída com os atributos corretos | 3 horas | 14 horas | Caio, Eduardo, Gabriel |
| 3       | [excluído]Correção dos dados: SpLink | N/A | N/A | N/A |
| 3       | [novo]Alterar no TAP a data das entregas | 0.1 horas | 0.1 horas | Eduardo |
| 3       | [novo]Arrumar bug na planilha de entrada | 2 horas | 0.5 hora | Gabriel |
| 3       | Gerar uma planilha dos dados do Flora e PlantList | 3 horas | 0.5 hora | Gabriel |
| 4 | Correção dos dados de entrada | 10.5 horas | 0.5 hora | Caio |
| 4 | [novo]Realizar casos de teste | 3 horas | 1.5 hora | Caio |
| 4 | [novo]Gerar planilha do GBIF e THEPLANTLIST | 3 horas | 1.5 hora | Gabriel |
| 4 | [novo]Gerar o executável do programa | 1 hora | 0.03 hora | Gabriel |
| 4 | [novo]Realizar maior cobertura de testes no script Flora do Brasil | 2 horas | 2 horas | Caio |
| 4 | [novo]Realizar maior cobertura de testes no script GBIF | 2 horas | 2 horas | Eduardo |
| 4 | [novo]Incluir apenas os nomes aceitos na Planilha 2 | 1 hora | 0.5 hora | Gabriel |
|1,2,3,4|Total|77.6|82.5||
