from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pywhatkit
import time


class Automation:
    def __init__(self):
        self.service = Service(executable_path="chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.service)
        self.search_link = 'https://google.com'
        self.news_link = {'Sports': 'https://www.thesun.co.uk/sport/',
                          'Tech': 'https://techcrunch.com/',
                          'Science': 'https://www.wired.com/category/science/',
                          'Entertainment': 'https://www.tmz.com/',
                          'Games': 'https://in.ign.com/'}

    def search(self, query, wait_time=5):
        self.driver.get(self.search_link)
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

    def get_tech_news(self):
        self.driver.get(self.news_link['Tech'])
        x_path = '//a[@class="post-block__title__link"]'
        containers = self.driver.find_elements(by='xpath', value=x_path)
        for container in containers:
            try:
                title = container.text
                link = container.get_attribute('href')
                print(f'Title: {title}\nLink: {link}\n')
            except Exception as e:
                continue

    def get_sports_news(self):
        self.driver.get(self.news_link['Sports'])
        x_path = '//div[@class="teaser__copy-container"]'
        containers = self.driver.find_elements(by='xpath', value=x_path)
        news = []
        for container in containers:
            try:
                title = container.find_element(by='xpath', value='./a/h3').text
                sub_title = container.find_element(by='xpath', value='./a/p').text
                link = container.find_element(by='xpath', value='./a').get_attribute('href')
                print(f'Title: {title}\nSub Title: {sub_title}\nLink: {link}\n')
                news.append(sub_title)
                if len(news)>2:
                    return news
                                
            except Exception as e:
                continue
            
    def send_message(self, phone_no, time: list, message: str, code='+91'):
        pywhatkit.sendwhatmsg(phone_no=code+phone_no, message=message,
                              time_hour=time[0], time_min=time[1],)

    
    def close(self):
        self.driver.quit()


def main():
    automation = Automation()
    # automation.search(query='Python Programming Language')
    automation.get_entertainment_news()
    automation.close()
    # time = [12, 23]
    # automation.send_message(phone_no="xxxxxxxxxx",
    #                         time=time, message="HELLOOO FROM THE OTHER SIDE")


if __name__ == "__main__":
    main()
