"""Gera o arquivo `Empresas` com todas as empresas listadas na B3.

Primeiro passo da coleta: o main.py lê este arquivo. Código extraído
do rascunho original em Testes/sel-tests.py.
Execute dentro da pasta Main: python coletar_empresas.py
"""
from time import sleep

from Classes import B3
from Functions import storage_empresas

driver = B3()

driver.get(
    "http://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/"
    "renda-variavel/empresas-listadas.htm"
)

driver.go_to_frame("bvmf_iframe")

sleep(5)

# Botão "Todas": lista todas as empresas na mesma página
driver.execute_script(
    'return document.getElementById("ctl00_contentPlaceHolderConteudo_'
    'BuscaNomeEmpresa1_btnTodas").click()'
)

sleep(5)

storage_empresas(driver)

sleep(10)
driver.close()
driver.quit()
