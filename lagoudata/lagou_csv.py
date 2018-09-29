import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class Lagou(object):
    def __init__(self, search_name):
        self.start_url = "https://www.lagou.com/jobs/list_{}?px=default&city=%E5%8C%97%E4%BA%AC#filterBox"
        self.search_name = search_name
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        self.content_header = ["positionName", "businessZones", "CreateTime", "companyShortName", "salary", "workYear"]

    def get_content_list(self):  # 提取数据
        li_list = self.driver.find_elements_by_xpath('//li[contains(@class, "con_list_item")]')
        content_list = []
        for li in li_list:
            item_list = []
            item_list.append(li.find_element_by_tag_name("h3").text)
            item_list.append(li.find_element_by_tag_name("em").text)
            item_list.append(li.find_elements_by_xpath(".//span[@class='format-time']")[0].text)
            item_list.append(li.find_elements_by_xpath(".//div[@class='company_name']")[0].text)
            item_list.append(li.find_elements_by_xpath(".//span[@class='money']")[0].text)
            item_list.append(li.find_elements_by_xpath(".//div[@class='li_b_l']")[0].text)

            # print(item_list)
            content_list.append(item_list)

        # 下一页
        next_url = self.driver.find_elements_by_xpath("//span[@class='pager_next ']")
        next_url = next_url[0] if len(next_url) > 0 else None
        return content_list, next_url

    def save_content_list(self, content_list):
        with open(self.search_name + "_data.csv", "a", encoding='utf-8') as f:
            for content in content_list:
                print(content)
                for item in content:
                    if isinstance(item, str):
                        if '，' in item:
                            item.replace(",", "|")
                    f.write(item + ",")
                f.write('\n')

    def run(self):
        # 发送请求
        self.driver.get(self.start_url.format(self.search_name))

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
    lagou = Lagou("python")
    lagou.run()
    # 翻页
