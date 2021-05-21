from time import sleep

from Classes import *
from Functions import *

print("Running Main/main.")

empresas = get_empresas()

driver = B3()  # Tem que estar com o gerenciador de tarefas fechado

for i in range(len(empresas)):
    url = "http://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/empresas-listadas.htm"
    driver.get(url)

    driver.go_to_frame("bvmf_iframe")

    # Digita e busca
    search_field_id = "ctl00_contentPlaceHolderConteudo_BuscaNomeEmpresa1_txtNomeEmpresa_txtNomeEmpresa_text"
    driver.sk(search_field_id, empresas[i])

    search_button_id = "ctl00_contentPlaceHolderConteudo_BuscaNomeEmpresa1_btnBuscar"
    driver.c(search_button_id)

    # print(driver.texts("GridRow_SiteBmfBovespa", False), empresas[i])

    # Seleciona Empresa
    driver.c('//*[@id="ctl00_contentPlaceHolderConteudo_BuscaNomeEmpresa1_grdEmpresa_ctl01"]/tbody/tr/td[1]/a', False)

    # Seleciona Formulário de Referência
    driver.c('ctl00_contentPlaceHolderConteudo_MenuEmpresasListadas1_tabMenuEmpresa_tabRelatoriosFinanceiros')

    # Anos para análise
    items = driver.itens("ctl00_contentPlaceHolderConteudo_cmbAno")
    anos = [item.text for item in items.options]

    # Acessa cada ano
    for j in range(2, len(items.options) + 1):
        driver.c(f'//*[@id="ctl00_contentPlaceHolderConteudo_cmbAno"]/option[{j}]', False)

        # Pega o Formulário de Referência
        sleep(5)  # Pode dar problema aqui
        try:
            formulario = driver.find_element_by_id(
                "ctl00_contentPlaceHolderConteudo_rptDocumentosFRE_ctl00_lnkDocumento"
            ).get_attribute("href")
        except Exception:
            formulario = None
        # print(formulario, len(formulario))

        while True:
            try:
                if formulario is not None:
                    # Entra com um driver filho no link do Formulário de Referência
                    driver_filho = B3()
                    driver_filho.get(formulario.split("'")[1])

                    # Vai até os diretores
                    driver_filho.c('//*[@id="cmbGrupo"]/option[12]', False)
                    driver_filho.c('//*[@id="cmbQuadro"]/option[5]', False)

                    # Entra no iframe dos diretores
                    url_retorno = driver_filho.execute_script(
                        "return document.getElementById('iFrameFormulariosFilho').contentWindow.location.href"
                    )
                    driver_filho.get(url_retorno)

                    diretores_bruto = driver_filho.texts('labelOld', False)
                    diretores_tratado = [diretores for diretores in diretores_bruto if diretores != ""]

                    print(empresas[i])
                    print(anos[j - 1])
                    for k in range(0, len(diretores_tratado), 3):
                        print(f'{diretores_tratado[k]} || {diretores_tratado[k + 1]} || {diretores_tratado[k + 2]}')

                    driver_filho.close()
                    driver_filho.quit()
                else:
                    break

                break
            except Exception as e:
                print(e)
    sleep(5)

sleep(10)
driver.close()
driver.quit()
