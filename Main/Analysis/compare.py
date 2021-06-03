"""Lista as empresas que ainda não aparecem nos dados coletados.

Execute a partir da raiz do projeto: python -m Main.Analysis.compare
"""
from pathlib import Path

import pandas as pd

from Main.Functions import get_empresas

MAIN_DIR = Path(__file__).resolve().parent.parent  # pasta Main/

header_list = ["Empresa", "Ano", "Nome", "CPF", "Cargo"]

# Arquivo gerado pelo main.py (separado por ";")
df = pd.read_csv(
    MAIN_DIR / "data",
    sep=";",
    on_bad_lines="skip",
    names=header_list
)

empresas_analisadas = set(df["Empresa"].to_list())
empresas_a_analisar = get_empresas(MAIN_DIR / "Empresas")

restantes = [
    empresa
    for empresa in empresas_a_analisar
    if empresa not in empresas_analisadas
]

for empresa in restantes:
    print(empresa)
