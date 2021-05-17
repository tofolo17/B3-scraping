from time import sleep

from selenium import webdriver

driver = webdriver.Chrome('/Users/tofol/Downloads/chromedriver')

url = "https://www.rad.cvm.gov.br/ENETCONSULTA/frmGerenciaPaginaFRE.aspx?NumeroSequencialDocumento=104273&CodigoTipoInstituicao=2"
driver.get(url)

sleep(5)

url_retorno = driver.execute_script(
    "return document.getElementById('iFrameFormulariosFilho').contentWindow.location.href"
)

driver.get(url_retorno)

elements = driver.find_elements_by_class_name("labelOld")
for i in range(len(elements)):
    if i % 2 == 0:
        f_name = "Name"
    else:
        f_name = "Cargo"
    with open(f_name, "a") as f:
        f.write(elements[i].text + "\n")

driver.close()
driver.quit()
