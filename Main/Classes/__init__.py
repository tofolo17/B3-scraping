import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

options = Options()


# options.add_argument('--headless')


class B3(webdriver.Chrome):
    def __init__(self):
        super().__init__(
            executable_path=os.environ.get("DRIVER_PATH"),
            options=options
        )

    def go_to_frame(self, frame):
        while True:
            try:
                self.switch_to.frame(self.find_element_by_id(frame))
                break
            except Exception:
                pass

    def sk(self, field, key):
        while True:
            try:
                self.find_element_by_id(field).send_keys(key)
                break
            except Exception:
                pass

    def c(self, field, via_id=True):
        while True:
            try:
                if via_id:
                    self.execute_script(f"document.getElementById('{field}').click()")
                    break
                else:
                    self.find_element_by_xpath(field).click()
                    break
            except Exception:
                pass

    def texts(self, field, via_id=True):
        while True:
            try:
                if via_id:
                    values = self.find_elements_by_id(field)
                else:
                    values = self.find_elements_by_class_name(field)
                if values is not None and len(values) != 0:
                    name_list = [value.text for value in values]
                    return name_list
            except Exception:
                pass

    def get_href(self, field):
        while True:
            try:
                reference = self.find_element_by_id(field).get_attribute('href')
                reference_link = reference.split("'")[1]
                return reference_link
            except Exception:
                pass

    def itens(self, field):
        while True:
            try:
                select = Select(self.find_element_by_id(field))
                return select
            except Exception:
                pass
