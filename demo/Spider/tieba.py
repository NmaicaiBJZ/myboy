import requests
from lxml import etree
import json
import os

class TiebaSpider:
    def __init__(self,tiebaname):
        self.tiebaname = tiebaname
        self.part_url = "http://tieba.baidu.com/mo/q---1E1A44492752A8CFE48A31DB2C0BB8FE:FG=1--1-3-0--2--wapp_1536855175546_700/"
        self.start_url = "http://tieba.baidu.com/mo/q---1E1A44492752A8CFE48A31DB2C0BB8FE:FG=1--1-3-0--2--wapp_1536855175546_700/m?kw="+tiebaname+"&pn=0"
        self.headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36"}


    def parse_url(self,url): #发送请求
        print(url)
        response = requests.get(url,self.headers)
        return response.content


    def get_content_list(self,html_str): #提取数据
        html = etree.HTML(html_str)
        div_list = html.xpath("//div[contains(@class,'i')]") #将class包含i的div分组
        content_list = []
        for div in div_list:
            item = {}
            item["title"] = div.xpath("./a/text()")[0] if len(div.xpath("./a/text()"))>0 else None
            item["href"] = self.part_url+div.xpath("./a/@href")[0] if len(div.xpath("./a/@href"))>0 else None
            item["img_list"] = self.get_img_list(item["href"],[])
            item["img_list"] = [requests.utils.unquote(i).split("src=")[-1] for i in item["img_list"]]
            content_list.append(item)
        #提取下一页的url地址
        next_url = self.part_url+html.xpath("//a[text()='下一页']/@href")[0] if len(html.xpath("//a[text()='下一页']/@href")) else None
        return content_list,next_url


    def get_img_list(self,detail_url,totol_img_list): #获取帖子中的所有图片
        #请求列表页的url地址，获取详情页的第一页
        detail_html_str = self.parse_url(detail_url)
        detail_html = etree.HTML(detail_html_str)
        #提取详情页第一页的图片，获取下一页的地址
        img_list = detail_html.xpath("//a[text()='图']/@href") 
        totol_img_list.extend(img_list) # 将图片的url地址放入列表中
        #请求详情页下一页的地址，进入循环
        detail_next_url = detail_html.xpath("//a[text()='下一页']/@href")
        if len(detail_next_url)>0:
            detail_next_url = self.part_url+detail_next_url[0]
            return self.get_img_list(detail_next_url,totol_img_list) # 递归，反复调用直到没有下一页为止
        
        return totol_img_list

    
    def save_content_list(self,content_list):
        file_name = self.tiebaname+".txt"
        with open(file_name,"a",encoding='utf-8') as f:
            for content in content_list:
                f.write(json.dumps(content,ensure_ascii=False,indent=2))
                f.write("\n")
        print("保存成功,路径：{}".format(os.getcwd()))

    def save_img(self,content_list):
        i = 0
        for content in content_list:
            if content["img_list"]:
                for img_ur in content["img_list"]:
                    i += 1
                    file_name = self.tiebaname+str(i)+".jpg"
                    with open(file_name,"wb") as f:
                        f.write(self.parse_url(img_ur))
                        print("保存图片成功"+file_name)
                


    def run(self):
        next_url = self.start_url #将刚开始的url地址给下一个
        while next_url is not None:
            html_str = self.parse_url(next_url) #发送请求 ，获取相应

            #提取数据，提取下一页的URL地址
            content_list,next_url = self.get_content_list(html_str)
            #保存数据
            self.save_content_list(content_list)
            #请求下一页url地址
            self.save_img(content_list) #保存图片


if __name__ == "__main__":
    tiebast = TiebaSpider("大吉岭")
    tiebast.run()
