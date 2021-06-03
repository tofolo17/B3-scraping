def storage_empresas(d):  # precisa estar no iframe
    elementos_empresa = []
    while len(elementos_empresa) == 0:
        elementos_empresa = d.find_elements_by_class_name("GridRow_SiteBmfBovespa") + \
                            d.find_elements_by_class_name("GridAltRow_SiteBmfBovespa")

    with open("Empresas", "a", encoding="utf-8") as f:
        for empresa in elementos_empresa:
            texto_interno = empresa.find_element_by_xpath("./td[1]/a").text
            f.write(f"{texto_interno}\n")


def get_empresas(path):
    with open(path, "r", encoding="utf-8") as f:
        lista_empresas = [line.strip("  \n") for line in f.readlines()]
    return sorted(lista_empresas)
