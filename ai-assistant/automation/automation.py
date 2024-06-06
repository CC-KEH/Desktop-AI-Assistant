from urllib import request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pywhatkit
from saved_data.constants import *
from credentials.credentials import news_api_key
import json

class Automation:
    def __init__(self):
        self.service = Service(executable_path="chromedriver.exe")
        self.search_link = search_link
        self.options = Options()
        self.driver = None
        
    def search(self, query, wait_time=5):
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
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

    def get_news_data(self, topic='', news_type='top-headlines'):
        articles = {}
        url = f'https://newsapi.org/v2/{news_type}?q={topic}&apiKey={news_api_key}'
        response = request.urlopen(url)
        data = json.load(response)
        for article in data['articles']:
            if article['source']['name'] == '[Removed]' or article['title'] == '[Removed]':
                continue
            articles[article['source']['name']] = article['title']
        return articles
    
    def get_news(self,topic='science'):
        articles = self.get_news_data(topic)
        return articles
                
    def send_message(phone_no, time, message: str, code='+91'):
        print("hour", time.hour, "minute", time.minute)
        hour = time.hour
        minute = time.minute+2
        pywhatkit.sendwhatmsg(phone_no=code+phone_no, message=message,
                              time_hour=hour, time_min=minute,)
    
    def close(self):
        if self.driver:
            self.driver.quit()


def main():
    automation = Automation()
    # automation.search(query='Python Programming Language')
    automation.get_news()
    automation.close()
    # time = [12, 23]
    # automation.send_message(phone_no="xxxxxxxxxx",
    #                         time=time, message="HELLOOO FROM THE OTHER SIDE")


if __name__ == "__main__":
    main()
