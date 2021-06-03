"""Funções auxiliares para a lista de empresas listadas na B3."""
from selenium.webdriver.common.by import By


def storage_empresas(d):
    """Salva no arquivo `Empresas` os nomes da tabela de empresas.

    Precisa ser chamada com o driver já dentro do iframe da B3.
    """
    elementos_empresa = []
    # Linhas pares e ímpares da tabela têm classes diferentes
    while len(elementos_empresa) == 0:
        elementos_empresa = (
            d.find_elements(By.CLASS_NAME, "GridRow_SiteBmfBovespa")
            + d.find_elements(By.CLASS_NAME, "GridAltRow_SiteBmfBovespa")
        )

    with open("Empresas", "a", encoding="utf-8") as f:
        for empresa in elementos_empresa:
            texto_interno = empresa.find_element(By.XPATH, "./td[1]/a").text
            f.write(f"{texto_interno}\n")


def get_empresas(path):
    """Lê o arquivo de empresas (uma por linha) em ordem alfabética."""
    with open(path, "r", encoding="utf-8") as f:
        lista_empresas = [line.strip("  \n") for line in f.readlines()]

    return sorted(lista_empresas)
