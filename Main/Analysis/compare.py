import pandas as pd

from Main.Functions import get_empresas

header_list = ["Empresa", "Ano", "Nome", "CPF", "Cargo"]
df = pd.read_csv(
    "C:/Users/tofol/Documents/GitHub/B3Scraping/Main/data.csv",
    sep=";",
    error_bad_lines=False,
    names=header_list
)

empresas_analisadas = set(df["Empresa"].to_list())
empresas_a_analisar = get_empresas("C:/Users/tofol/Documents/GitHub/B3Scraping/Testes/Empresas")

restantes = [empresa for empresa in empresas_a_analisar if empresa not in empresas_analisadas]

for empresa in restantes:
    print(empresa)
