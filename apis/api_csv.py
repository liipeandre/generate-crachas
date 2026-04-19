import sys as sys
import pandas as pandas


def load_csv():

    # Carregando o CSV de entrada
    if len(sys.argv) < 2:
        raise ValueError("Por favor, forneça o caminho para o arquivo CSV como argumento.")

    # Carregar dados do CSV
    path = sys.argv[1]

    try:
        dataframe = pandas.read_csv(path, dtype=str)
        dataframe = dataframe.astype(str)

    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo CSV não encontrado em {path}")

    return dataframe
