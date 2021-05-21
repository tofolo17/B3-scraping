import urllib.request

from bs4 import BeautifulSoup

# url = "https://www.rad.cvm.gov.br/ENETCONSULTA/frmGerenciaPaginaFRE.aspx?" \
#      "NumeroSequencialDocumento=104273&CodigoTipoInstituicao=2"

url = "https://www.rad.cvm.gov.br/ENETCONSULTA/frmResponsavelConteudoFormularioFRENovo.aspx?Grupo=1.+Respons%c3%a1veis+pelo+formul%c3%a1rio&Quadro=1.0+-+Identifica%c3%a7%c3%a3o&NomeTipoDocumento=FRE%20NOVO&Empresa=ITAU%20UNIBANCO%20HOLDING%20S.A.&DataReferencia=2020-01-01&Versao=21&CodTipoDocumento=8&NumeroSequencialDocumento=104273&NumeroSequencialRegistroCvm=1865&CodigoTipoInstituicao=2&Hash=2n7zILxblkyM2spnVmfOdOC7vZE24qRwBMcsoXHY"

html_doc = urllib.request.urlopen(url)

soup = BeautifulSoup(html_doc.read(), "html.parser")

print(soup.prettify())

print(soup.find(value=353))

# print(soup.prettify())

"""print(soup.iframe)

iframes = soup.find_all('iframe')

for iframe in iframes:
    response = urllib.request.urlopen(iframe.attrs['src'])
    iframe_soup = BeautifulSoup(response)
    
for iframe in iframes:
    print(iframe.extract())"""

"""iframe = soup.select_one("#iFrameFormulariosFilho")

print(iframe)"""
