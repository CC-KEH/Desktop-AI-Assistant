from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Automation:
    def __init__(self):
        self.service = Service(executable_path="chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.service)

    def search(self, query, wait_time=5):
        self.driver.get('https://google.com')
        WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
        )
        input_element = self.driver.find_element(By.CLASS_NAME, "gLFyf")
        input_element.clear()
        input_element.send_keys(query + Keys.ENTER)
        WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, query))
        )
        link = self.driver.find_element(By.PARTIAL_LINK_TEXT, query)
        link.click()

    def close(self):
        self.driver.quit()


def main():
    automation = Automation()
    automation.search(query='Tech With Tim')
    automation.close()


if __name__ == "__main__":
    main()
