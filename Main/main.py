"""Coleta os diretores de cada empresa nos Formulários de Referência.

Para cada empresa do arquivo `Empresas`, abre a página da B3, percorre
os anos a partir de 2010 e grava no arquivo `data` uma linha por
diretor: Empresa;Ano;Nome;CPF;Cargo.

Pode ser que algumas empresas não tenham sido acessadas. Verificar
posteriormente com Analysis/compare.py.
"""
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from Classes import B3
from Functions import get_empresas

URL_EMPRESAS = (
    "http://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/"
    "renda-variavel/empresas-listadas.htm"
)
PREFIXO = "ctl00_contentPlaceHolderConteudo_"  # prefixo dos ids da B3

print("Running Main/main.")

empresas = get_empresas("Empresas")

for i in range(len(empresas)):
    driver = B3()  # Tem que estar com o gerenciador de tarefas fechado

    driver.get(URL_EMPRESAS)
    driver.go_to_frame("bvmf_iframe")

    # Digita e busca
    search_field_id = (
        PREFIXO + "BuscaNomeEmpresa1_txtNomeEmpresa_txtNomeEmpresa_text"
    )
    driver.sk(search_field_id, empresas[i])
    search_button_id = PREFIXO + "BuscaNomeEmpresa1_btnBuscar"
    driver.c(search_button_id)

    # Seleciona Empresa
    driver.c(
        f'//*[@id="{PREFIXO}BuscaNomeEmpresa1_grdEmpresa_ctl01"]'
        '/tbody/tr/td[1]/a',
        False
    )

    # Seleciona Formulário de Referência
    driver.c(
        PREFIXO
        + "MenuEmpresasListadas1_tabMenuEmpresa_tabRelatoriosFinanceiros"
    )

    # Anos para análise
    items = driver.itens(PREFIXO + "cmbAno")
    anos = [item.text for item in items.options]

    # Acessa cada ano (a 1ª opção do select não é um ano)
    for j in range(2, len(items.options) + 1):
        if int(anos[j - 1]) >= 2010:
            driver.c(
                f'//*[@id="{PREFIXO}cmbAno"]/option[{j}]', False
            )

            # Pega o Formulário de Referência
            try:
                elemento_formulario = WebDriverWait(driver, 10).until(
                    ec.element_to_be_clickable((
                        By.ID,
                        PREFIXO + "rptDocumentosFRE_ctl00_lnkDocumento"
                    ))
                )
                formulario = elemento_formulario.get_attribute("href")
            except Exception as e:
                print(f"Sem formulário: {e}")
                formulario = None

            # Repete até conseguir extrair os diretores deste ano
            while True:
                try:
                    if formulario is not None:
                        # Entra com um driver filho no link do Formulário
                        # de Referência (href no formato javascript:...)
                        driver_filho = B3()
                        driver_filho.get(formulario.split("'")[1])

                        # Vai até os diretores (grupo 12 do formulário)
                        driver_filho.c(
                            '//*[@id="cmbGrupo"]/option[12]', False
                        )
                        sleep(1)

                        index = 0
                        options = driver_filho.itens('cmbQuadro')
                        for option in options.options:
                            if "Composição e experiência" in option.text:
                                index = options.options.index(option) + 1
                                break

                        driver_filho.c(
                            f'//*[@id="cmbQuadro"]/option[{index}]', False
                        )

                        # Entra no iframe dos diretores
                        url_retorno = driver_filho.execute_script(
                            "return document.getElementById("
                            "'iFrameFormulariosFilho')"
                            ".contentWindow.location.href"
                        )
                        driver_filho.get(url_retorno)

                        # Pega os dados dos diretores: a tabela vem como
                        # uma lista plana [nome, cpf, cargo, nome, ...]
                        diretores_bruto = driver_filho.texts(
                            'TdTamanho300', False
                        )
                        diretores_final = [
                            diretores for diretores in diretores_bruto[3:]
                        ]

                        # Tentativa (desativada) de coletar a idade
                        """
                        info_spec = []

                        # Informações específicas
                        qtd_diretores = floor(len(diretores_final) / 3)
                        for k in range(1, qtd_diretores + 1):
                            print(k, qtd_diretores)
                            while True:
                                try:
                                    plus_element = driver_filho.find_element(
                                        By.ID, f"imgSetaFiltro{k}"
                                    )
                                    plus_element.click()

                                    sleep(0.5)

                                    break
                                except Exception:
                                    pass

                        for k in range(1, qtd_diretores + 2):
                            while True:
                                try:
                                    if k != 1:
                                        data = driver_filho.find_element(
                                            By.XPATH,
                                            f'/html/body/form/div[3]/table/'
                                            f'tbody/tr[{(k - 1) * 2}]/td[2]/'
                                            f'div/div/table/tbody/tr/td[2]/'
                                            f'table/tbody/tr[1]/td[2]/span '
                                        )
                                        info_spec.append(
                                            data.text
                                            if (data.text != ""
                                                and "/" in data.text)
                                            else "Não informado."
                                        )  # Idade, quando não tem "/"
                                        break
                                    break
                                except Exception:
                                    pass

                        print(info_spec)
                        """

                        with open("data", "a", encoding="utf-8") as f:
                            # Informações gerais (3 campos por diretor)
                            for k in range(0, len(diretores_final), 3):
                                print(k)
                                cpf = diretores_final[k + 1]
                                if cpf == "":
                                    cpf = "Não informado."
                                f.write(
                                    f'{empresas[i]};'  # Empresa
                                    f'{anos[j - 1]};'  # Ano
                                    f'{diretores_final[k]};'  # Nome
                                    f'{cpf};'  # CPF
                                    f'{diretores_final[k + 2]}\n'  # Cargo
                                    # f'{info_spec[int(k / 3)]}\n'
                                )

                        driver_filho.close()
                        driver_filho.quit()

                    break
                except Exception as e:
                    print(e)

    sleep(2)

    driver.close()
    driver.quit()
