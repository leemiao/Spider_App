import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class Lagou(object):
    def __init__(self):
        self.start_url = "https://www.lagou.com/jobs/list_python?px=default&city=%E5%8C%97%E4%BA%AC#filterBox"
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)

    def get_content_list(self): # 提取数据
        liList = self.driver.find_elements_by_xpath('//li[contains(@class, "con_list_item")]')
        content_list = []
        for li in liList:
            item = {}

            item['positionName'] = li.find_element_by_tag_name("h3").text
            item['businessZones'] = li.find_element_by_tag_name("em").text
            item['CreateTime'] = li.find_elements_by_xpath(".//span[@class='format-time']")[0].text
            item['companyShortName'] = li.find_elements_by_xpath(".//div[@class='company_name']")[0].text
            item['salary'] = li.find_elements_by_xpath(".//span[@class='money']")[0].text
            item['workYear'] = li.find_elements_by_xpath(".//div[@class='li_b_l']")[0].text
            # print(item)

            content_list.append(item)

        # 下一页
        next_url = self.driver.find_elements_by_xpath("//span[@class='pager_next ']")
        next_url = next_url[0] if len(next_url) > 0 else None
        return content_list, next_url

    def save_content_list(self, content_list):
        for content in content_list:
            content = json.dumps(content, ensure_ascii=False)
            print(content)
            with open("lagoudata.txt", "a", encoding='utf-8') as f:
                f.write(content + "/n")

    def run(self):
        # 发送请求
        self.driver.get(self.start_url)
        # 提取数据
        content_list, next_url = self.get_content_list()
        # 保存数据
        self.save_content_list(content_list)
        # 翻页
        while next_url is not None:
            next_url.click()
            time.sleep(6)
            content_list, next_url = self.get_content_list()
            self.save_content_list(content_list)

if __name__ == '__main__':
    lagou = Lagou()
    lagou.run()
    # 翻页










