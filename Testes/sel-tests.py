"""Rascunho: experimentos com Selenium na página de diretores da CVM.

Testa a abertura de um Formulário de Referência e a expansão dos
detalhes de cada diretor (base da coleta de idade, desativada no main).
Execute a partir da raiz do projeto: python Testes/sel-tests.py
"""
import sys
from pathlib import Path
from time import sleep

from selenium.webdriver.common.by import By

# Permite importar o pacote Main ao rodar o arquivo diretamente
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from Main.Classes import B3  # noqa: E402

# Primeira versão (desativada), antes da classe B3
"""
from selenium import webdriver

driver = webdriver.Chrome()

url = (
    "https://www.rad.cvm.gov.br/ENETCONSULTA/frmGerenciaPaginaFRE.aspx?"
    "NumeroSequencialDocumento=104273&CodigoTipoInstituicao=2"
)
driver.get(url)

sleep(5)

url_retorno = driver.execute_script(
    "return document.getElementById('iFrameFormulariosFilho')"
    ".contentWindow.location.href"
)

driver.get(url_retorno)

elements = driver.find_elements(By.CLASS_NAME, "labelOld")
for i in range(len(elements)):
    if i % 2 == 0:
        f_name = "Name"
    else:
        f_name = "Cargo"
    with open(f_name, "a") as f:
        f.write(elements[i].text + "\\n")

driver.close()
driver.quit()
"""

print("Running Testes/sel-tests")

driver = B3()

driver.get(
    "https://www.rad.cvm.gov.br/ENETCONSULTA/frmGerenciaPaginaFRE.aspx?"
    "NumeroSequencialDocumento=104631&CodigoTipoInstituicao=2"
)

# Grupo 12 (administração) > quadro 5 (composição dos diretores)
driver.c('//*[@id="cmbGrupo"]/option[12]', False)
driver.c('//*[@id="cmbQuadro"]/option[5]', False)

sleep(2)

url_retorno = driver.execute_script(
    "return document.getElementById('iFrameFormulariosFilho')"
    ".contentWindow.location.href"
)

driver.get(url_retorno)

sleep(2)

# Botões "+" que expandem os detalhes de cada diretor
plus_elements = driver.find_elements(By.CLASS_NAME, "TdTamanho20")

for i in range(1, len(plus_elements)):
    plus_elements[i - 1].click()
    sleep(2)

    if i != 1:
        print(i * 2 if i != 0 else 0)
        data = driver.find_element(
            By.XPATH,
            f'/html/body/form/div[3]/table/tbody/tr[{(i - 1) * 2}]/td[2]/'
            'div/div/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/span '
        )
        print(data.text)

sleep(20)

driver.close()
driver.quit()
