import requests
from selenium import webdriver
import time
import json
import os 

class douyuSpider():
    def __init__(self):
        self.start_url = "https://www.douyu.com/directory/all"
        self.driver = webdriver.Chrome()


    def get_content_list(self):
        time.sleep(4)
        li_list = self.driver.find_elements_by_xpath("//ul[@class='layout-Cover-list']/li")
        item_list = []
        for li in li_list:
            item = {}
            item["room_title"] = li.find_element_by_xpath(".//div[@class='DyListCover-content']//span[@class='DyListCover-zone']").text
            item["room_value"] = li.find_element_by_xpath(".//div[@class='DyListCover-content']//h3").text
            item["room_username"] = li.find_element_by_xpath(".//div[@class='DyListCover-content']//div[@class='DyListCover-userName']").text
            item["room_img"] = li.find_element_by_xpath(".//div[@class='DyListCover-imgWrap']/div/img").get_attribute("src")
            print(item)
            item_list.append(item)
    
        next_url = self.driver.find_elements_by_xpath("//li[@class=' dy-Pagination-next']")
        next_url = next_url[0] if len(next_url)>0 else None
        # print(next_url.text)

        return item_list,next_url

    
    def save_content_list(self,content_list):
        with open("douyu.json","a",encoding='utf-8') as f:
            f.write(json.dumps(content_list,ensure_ascii=False,indent=4))
            print("保存成功:文件位置{}".format(os.getcwd()))
            

    def run(self):
        # start_url
        self.driver.get(self.start_url)
        # 获取数据
        content_list,next_url = self.get_content_list()
        # 保存数据
        self.save_content_list(content_list)

        # 单击下一页元素，进入循环
        while next_url is not None:
            next_url.click()
            content_list,next_url = self.get_content_list()
            self.save_content_list(content_list)



    
if __name__ == "__main__":
    douyu = douyuSpider()
    douyu.run()