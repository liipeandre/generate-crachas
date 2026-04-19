# Generate Crachás

## Descrição

Este é um script desenvolvido em Python para geração de imagens frente e verso para impressão de crachás a partir de fotos de rostos tiradas no formato png.

## Requisitos

- Python 3
- Bibliotecas listadas no arquivo `requirements.txt`

## Como Executar

- Preencha o arquivo lista_funcionarios.csv com os dados do funcionário (matrícula, nome e cargo)

- Adicione a foto do rosto do funcionário com o número da matrícula do funcionário.

- Abra o terminal e rode o comando abaixo:

python generate_crachas.py .\lista_funcionarios.csv

- As duas imagens (frente e verso) do crachá gerado sairão na pasta output. Após isso, basta imprimir usando alguma impressora própria para isso.
