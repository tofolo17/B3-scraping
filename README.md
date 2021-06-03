# B3-scraping

> 🇧🇷 [Português](#português) · 🇺🇸 [English](#english)

## Português

### O que você encontrará neste repositório?

Script de web scraping construído com o framework [Selenium](https://www.selenium.dev/), responsável por extrair uma
quantidade massiva de dados do site da [Bolsa do Brasil](https://www.b3.com.br/pt_br/). Os dados são:

* Nomes das empresas cadastradas;
* Formulários de Referência;
* Nome, CPF e cargo eletivo de todos os diretores listados nos formulários (pra cada ano, de cada empresa).

Tais dados foram fornecidos à [Fundação Dom Cabral](https://www.fdc.org.br/), mediante a orientação do Professor
[Paul Ferreira](https://br.linkedin.com/in/paulferreira) que, envolvido em projetos de iniciação científica, solicitou a
coleta.

Desenvolvido entre **maio e junho de 2021**. Projeto encerrado.

> 🔒 Os dados coletados vêm de documentos públicos da CVM, mas incluem dados pessoais (CPF). Por isso, nenhum dado
> coletado faz parte deste repositório.

### Ferramentas

* Python 3
* Selenium (navegação e extração)
* pandas (conferência dos dados coletados)
* BeautifulSoup (experimentos iniciais)

### Estrutura

```
├── Main/
│   ├── coletar_empresas.py  # passo 1: gera a lista de empresas (arquivo Empresas)
│   ├── main.py              # passo 2: coleta os diretores de cada empresa (arquivo data)
│   ├── Classes/             # driver B3: Chrome com atalhos para clicar, digitar e ler
│   ├── Functions/           # leitura e gravação da lista de empresas
│   └── Analysis/compare.py  # passo 3: lista empresas que ficaram sem dados
└── Testes/                  # rascunhos e experimentos do desenvolvimento
```

### Como usar

**1. Clone e instale as dependências** (requer o Google Chrome instalado)

```bash
git clone https://github.com/tofolo17/B3-scraping.git
cd B3-scraping
python -m venv .venv
# Windows: .venv\Scripts\activate | Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

O ChromeDriver é baixado automaticamente. Para usar um específico, defina a variável de ambiente `DRIVER_PATH` com o
caminho dele.

**2. Gere a lista de empresas e colete os dados**

```bash
cd Main
python coletar_empresas.py   # cria o arquivo Empresas (uma empresa por linha)
python main.py               # cria o arquivo data
```

O arquivo `data` tem uma linha por diretor, no formato `Empresa;Ano;Nome;CPF;Cargo`, com os anos a partir de 2010.

**3. Confira quais empresas faltaram** (a partir da raiz do projeto)

```bash
python -m Main.Analysis.compare
```

> ⚠️ O site da B3 mudou desde 2021, então os seletores podem não funcionar mais. Como o script repete cada ação até o
> elemento aparecer, um seletor desatualizado faz o programa ficar parado: nesse caso, interrompa com `Ctrl+C`.

### Licença

[MIT](LICENSE)

---

## English

### What will you find in this repository?

A web scraping script built with the [Selenium](https://www.selenium.dev/) framework, responsible for extracting a
massive amount of data from the [B3](https://www.b3.com.br/pt_br/) website. Extracted data:

* Company names;
* Reference Forms;
* Name, CPF (Brazilian taxpayer ID), and elected position of all directors on the forms (for each year and for each
  company).

Provided to [Dom Cabral Foundation](https://www.fdc.org.br/) under the guidance of Professor
[Paul Ferreira](https://br.linkedin.com/in/paulferreira), who requested it for future use in scientific initiation
projects.

Developed between **May and June 2021**. Project finished.

> 🔒 The collected data comes from public CVM filings but includes personal data (CPF). For that reason, no collected
> data is part of this repository.

### Tools

* Python 3
* Selenium (navigation and extraction)
* pandas (checking the collected data)
* BeautifulSoup (early experiments)

### Structure

```
├── Main/
│   ├── coletar_empresas.py  # step 1: builds the company list (Empresas file)
│   ├── main.py              # step 2: collects each company's directors (data file)
│   ├── Classes/             # B3 driver: Chrome with shortcuts to click, type and read
│   ├── Functions/           # reading and writing the company list
│   └── Analysis/compare.py  # step 3: lists companies left without data
└── Testes/                  # drafts and experiments from development
```

### How to use

**1. Clone and install the dependencies** (requires Google Chrome)

```bash
git clone https://github.com/tofolo17/B3-scraping.git
cd B3-scraping
python -m venv .venv
# Windows: .venv\Scripts\activate | Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

ChromeDriver is downloaded automatically. To use a specific one, set the `DRIVER_PATH` environment variable to its path.

**2. Build the company list and collect the data**

```bash
cd Main
python coletar_empresas.py   # creates the Empresas file (one company per line)
python main.py               # creates the data file
```

The `data` file has one line per director, formatted as `Empresa;Ano;Nome;CPF;Cargo` (company; year; name; CPF;
position), for years from 2010 on.

**3. Check which companies were missed** (from the project root)

```bash
python -m Main.Analysis.compare
```

> ⚠️ B3's website has changed since 2021, so the selectors may no longer work. Since the script retries each action until
> the element shows up, an outdated selector leaves the program stuck: in that case, stop it with `Ctrl+C`.

### License

[MIT](LICENSE)
