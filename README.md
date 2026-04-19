# Badge Generator (ou Gerador de Crachás)

## Descrição

Este script em Python automatiza a criação de crachás (frente e verso) prontos para impressão. Utilizando processamento de imagem e manipulação de dados, o sistema integra fotos de colaboradores com informações provenientes de um arquivo CSV, com a possibilidade de geração em lote, dispensando a necessidade de edições manuais.

## Principais funcionalidades:

- Processamento de Imagem: Identificação e manipulação de rostos utilizando OpenCV e Pillow.
- Automação em Lote: Gera múltiplos crachás de uma só vez a partir de uma base de dados.
- Saída Pronta para Impressão: Exporta arquivos formatados para impressoras térmicas ou de PVC.

## Requisitos

- Python 3
- Bibliotecas listadas no arquivo `requirements.txt`

## Como Executar

- Preencha o arquivo lista_funcionarios.csv com os dados de cada funcionário (matrícula, nome e cargo)

- Adicione a foto do rosto de cada funcionário com o número da matrícula do mesmo (ex: 1.png).

- Abra o terminal e rode o comando abaixo:

python generate_crachas.py .\lista_funcionarios.csv

- As duas imagens (frente e verso) do crachá gerado sairão na pasta output. Após isso, basta imprimir usando alguma impressora própria para isso.
