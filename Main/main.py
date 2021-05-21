from time import sleep

from Classes import *
from Functions import *

print("Running Main/main.")

empresas = get_empresas()

driver = B3()

for i in range(len(empresas)):
    url = "http://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/empresas-listadas.htm"
    driver.get(url)

    driver.go_to_frame("bvmf_iframe")

    # Digita e busca
    search_field_id = "ctl00_contentPlaceHolderConteudo_BuscaNomeEmpresa1_txtNomeEmpresa_txtNomeEmpresa_text"
    driver.sk(search_field_id, empresas[i])

    search_button_id = "ctl00_contentPlaceHolderConteudo_BuscaNomeEmpresa1_btnBuscar"
    driver.c(search_button_id)

    print(driver.texts("GridRow_SiteBmfBovespa"), empresas[i])

    # Seleciona Empresa
    driver.c('//*[@id="ctl00_contentPlaceHolderConteudo_BuscaNomeEmpresa1_grdEmpresa_ctl01"]/tbody/tr/td[1]/a', False)

    # Seleciona Formulário de Referência
    driver.c('ctl00_contentPlaceHolderConteudo_MenuEmpresasListadas1_tabMenuEmpresa_tabRelatoriosFinanceiros')

    # Anos para análise
    items = driver.itens("ctl00_contentPlaceHolderConteudo_cmbAno")

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
        print(formulario)

        while True:
            try:
                if formulario is not None:
                    # Entra com um driver filho no link do Formulário de Referência
                    driver_filho = B3()
                    driver_filho.get(formulario.split("'")[1])

                    # O que fazer dentro do Formulário de Referência
                    driver_filho.c('//*[@id="cmbGrupo"]/option[12]', False)
                    driver_filho.c('//*[@id="cmbQuadro"]/option[5]', False)

                    sleep(5)

                    driver_filho.close()
                    driver_filho.quit()
                else:
                    break

                break
            except Exception:
                pass
    sleep(5)

sleep(10)
driver.close()
driver.quit()
