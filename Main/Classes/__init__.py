"""Driver do Chrome com atalhos para navegar nas páginas da B3/CVM.

Os sites da B3 carregam elementos de forma lenta e irregular, por isso
cada método repete a ação até o elemento estar disponível.
"""
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

options = Options()


class B3(webdriver.Chrome):
    def __init__(self):
        # DRIVER_PATH é opcional: sem ele, o Selenium Manager baixa o
        # ChromeDriver compatível automaticamente
        super().__init__(
            service=Service(os.environ.get("DRIVER_PATH")),
            options=options
        )

    # Atenção: os métodos abaixo tentam indefinidamente (while True) até
    # a ação funcionar; se o seletor mudar no site, o script fica preso.

    def go_to_frame(self, frame):
        """Entra no iframe de id `frame`."""
        while True:
            try:
                self.switch_to.frame(self.find_element(By.ID, frame))
                break
            except Exception:
                pass

    def sk(self, field, key):
        """Digita `key` no campo de id `field` (send keys)."""
        while True:
            try:
                self.find_element(By.ID, field).send_keys(key)
                break
            except Exception:
                pass

    def c(self, field, via_id=True):
        """Clica num elemento por id (via JavaScript) ou por XPath."""
        while True:
            try:
                if via_id:
                    self.execute_script(
                        f"document.getElementById('{field}').click()"
                    )
                    break
                else:
                    self.find_element(By.XPATH, field).click()
                    break
            except Exception:
                pass

    def texts(self, field, via_id=True):
        """Devolve o texto de todos os elementos com o id/classe dado."""
        while True:
            try:
                if via_id:
                    values = self.find_elements(By.ID, field)
                else:
                    values = self.find_elements(By.CLASS_NAME, field)

                if values is not None and len(values) != 0:
                    name_list = [value.text for value in values]
                    return name_list
            except Exception:
                pass

    def get_href(self, field):
        """Extrai a URL de um link do tipo javascript:abrir('...')."""
        while True:
            try:
                reference = self.find_element(
                    By.ID, field
                ).get_attribute('href')
                reference_link = reference.split("'")[1]
                return reference_link
            except Exception:
                pass

    def itens(self, field):
        """Devolve o <select> de id `field` como objeto Select."""
        while True:
            try:
                select = Select(self.find_element(By.ID, field))
                return select
            except Exception:
                pass
