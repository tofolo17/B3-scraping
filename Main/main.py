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
        sleep(10)  # Pode dar problema aqui
        try:
            formulario = driver.find_element_by_id(
                "ctl00_contentPlaceHolderConteudo_rptDocumentosFRE_ctl00_lnkDocumento"
            ).get_attribute("href")
        except Exception:
            formulario = None

        while True:
            try:
                if formulario is not None:

                    # Entra com um driver filho no link do Formulário de Referência
                    driver_filho = B3()
                    driver_filho.get(formulario.split("'")[1])

                    # Vai até os diretores
                    driver_filho.c('//*[@id="cmbGrupo"]/option[12]', False)
                    sleep(2)

                    index = 0
                    options = driver_filho.itens('cmbQuadro')
                    for option in options.options:
                        if "Composição e experiência" in option.text:
                            index = options.options.index(option) + 1
                            break
                    driver_filho.c(f'//*[@id="cmbQuadro"]/option[{index}]', False)

                    # Entra no iframe dos diretores
                    url_retorno = driver_filho.execute_script(
                        "return document.getElementById('iFrameFormulariosFilho').contentWindow.location.href"
                    )
                    driver_filho.get(url_retorno)

                    # Pega os dados dos diretores
                    diretores_bruto = driver_filho.texts('TdTamanho300', False)
                    diretores_tratado = [diretores for diretores in diretores_bruto[3:]]

                    """
                    info_spec = []
                    # Informações específicas
                    qtd_diretores = floor(len(diretores_tratado) / 3)
                    for k in range(1, qtd_diretores + 1):
                        print(k, qtd_diretores)
                        while True:
                            try:
                                plus_element = driver_filho.find_element_by_id(f"imgSetaFiltro{k}")
                                plus_element.click()

                                sleep(0.5)

                                break
                            except Exception:
                                pass

                    for k in range(1, qtd_diretores + 2):
                        while True:
                            try:
                                if k != 1:
                                    data = driver_filho.find_element_by_xpath(
                                        f'/html/body/form/div[3]/table/tbody/tr[{(k - 1) * 2}]/td[2]/'
                                        f'div/div/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/span '
                                    )
                                    info_spec.append(
                                        data.text if (data.text != "" and "/" in data.text) else "Não informado."
                                    )  # Idade, quando não tem "/"
                                    break
                                break
                            except Exception:
                                pass
                    print(info_spec)
                    """

                    with open("data", "a", encoding="utf-8") as f:

                        # Informações gerais
                        for k in range(0, len(diretores_tratado), 3):
                            print(k)
                            f.write(
                                f'{empresas[i]};'  # Empresa
                                f'{anos[j - 1]};'  # Ano
                                f'{diretores_tratado[k]};'  # Nome
                                f'{diretores_tratado[k + 1] if diretores_tratado[k + 1] != "" else "Não informado."};'
                                #  CPF
                                f'{diretores_tratado[k + 2]}\n'  # Cargo eletivo ocupado
                                # f'{info_spec[int(k / 3)]}\n'
                            )

                    driver_filho.close()
                    driver_filho.quit()
                break
            except Exception as e:
                print(e)

sleep(10)
driver.close()
driver.quit()
