import requests
import json
import time

class bawangcan_Grab_tickets():
    def __init__(self):
        file = open('./data.json','r')
        read_jso = json.loads(file.read())
        file.close()
        User_Agent = read_jso['User_Agent']
        Token = read_jso['Token']
        self.headers={
            'User-Agent': User_Agent,
            'Token': Token,
            'Accept-Encoding': 'gzip, deflate',
            'Origin': 'https://h5.azhe.ac.cn',
            'Referer': 'https://h5.azhe.ac.cn/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Te': 'trailers',
            'Connection': 'close',
        }
        # 商家的距离 单位(m)
        self.Merchant_distance = read_jso['Merchant_distance']
        # 设置步长 越小抢票速度越快(单位秒)
        self.step_len = read_jso['step_len']
    # 获取店面的json数据
    # POST /tbms/c/activities/page HTTP/1.1
    # Host: h5.azhe.ac.cn
    # User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0
    # Accept: */*
    # Accept-Language: en-US,en;q=0.5
    # Accept-Encoding: gzip, deflate
    # Token: 3C79DBBD9F7D468690EF6053B87C0965
    # Content-Type: application/json
    # Content-Length: 173
    # Origin: https://h5.azhe.ac.cn
    # Referer: https://h5.azhe.ac.cn/
    # Sec-Fetch-Dest: empty
    # Sec-Fetch-Mode: cors
    # Sec-Fetch-Site: same-origin
    # Te: trailers
    # Connection: close
    # {"shopName":"","pageIndex":1,"pageSize":10,"type":0,"longitude":118.392009,"latitude":31.347711,"orderBy":"distance","mediaType":"-1","categoryId":-1,"favourableComment":-1}
    def get_lunch_data(self):
        # 获取数据的url地址
        get_data_url = "https://h5.azhe.ac.cn/tbms/c/activities/page"
        # 获取数据的请求json
        new_Merchant_data = []
        i = 1
        # 此循环的目的是重新获取商家的数据，过滤无用数据
        while(True):
            # pageSize 是一次性获取多少个商家的信息 pageIndex 翻页
            get_data_json = {"shopName":"","pageIndex":i,"pageSize":20,"type":0,"longitude":118.35703299444582,"latitude":31.284943881164143,"orderBy":"distance","mediaType":"-1","categoryId":-1,"favourableC omment":-1}
            re = requests.post(get_data_url,headers=self.headers,json=get_data_json)
            old_Merchant_data = json.loads(re.text)['data']['data']
            if(old_Merchant_data == []):
                return new_Merchant_data
            for j in old_Merchant_data:
                if(float(j['distance']) <= self.Merchant_distance and int(j['remainderJoinQuota']) > 0 and int(j['status']) < 3):
                    new_Merchant_data.append({'id':j['id'],'businessName':j['businessName'],'comment':j['comment'],'beginDate':j['beginDate'],'mediaTypeName':j['mediaTypeName'],'remainderJoinQuota':j['remainderJoinQuota'],'taskRuleUp':j['taskRuleUp'],'taskRuleReturn':j['taskRuleReturn'],'status':j['status'],'distance':j['distance']})
            i+=1

    # 抢票请求
    # POST /tbms/c/users/orders HTTP/1.1
    # Host: h5.azhe.ac.cn
    # User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0
    # Accept: */*
    # Accept-Language: en-US,en;q=0.5
    # Accept-Encoding: gzip, deflate
    # Token: 3C79DBBD9F7D468690EF6053B87C0965
    # Content-Type: application/json
    # Content-Length: 166
    # Origin: https://h5.azhe.ac.cn
    # Referer: https://h5.azhe.ac.cn/
    # Sec-Fetch-Dest: empty
    # Sec-Fetch-Mode: cors
    # Sec-Fetch-Site: same-origin
    # Te: trailers
    # Connection: close
    # {"activityId":243845,"longitude":118.35703299444582,"latitude":31.284943881164143,"address":"弋江区安徽师范大学皖江学院文津校区北门(文昌西路)"}
    def activity_request(self,activityID):
        activity_url="https://h5.azhe.ac.cn/tbms/c/users/orders"
        activity_post_data={"activityId":activityID,"longitude":118.35703299444582,"latitude":31.284943881164143,"address":"弋江区安徽师范大学皖江学院文津校区北门(文昌西路)"}
        re = requests.post(activity_url,headers=self.headers,json=activity_post_data)
        print(json.loads(re.text)['msg'])

    # 列出商家清单
    def display_Merchant_data(self,data):
        j = 1
        for i in data:
            print('序号ID: {0}\t商家:{1}\t需求:{2}\t开始时间:{3}\t外卖类型:{4}\t名额:{5}\t满{6}减{7}\t距离:{8}\n'.format(j,i['businessName'],i['comment'],i['beginDate'],i['mediaTypeName'],i['remainderJoinQuota'],i['taskRuleUp'],i['taskRuleReturn'],i['distance']))
            j += 1

    # 抢票
    def Grab_tickets(self,timing,activity_id):
        timing_hour,timing_min = [int(i) for i in timing.split(':')]
        while(True):
            t = time.localtime()
            if(t.tm_hour >= timing_hour and t.tm_min >= timing_min):
                self.activity_request(activity_id)
                break
            time.sleep(self.step_len)            
            print(f'当前系统时间为 {t.tm_hour} 时 {t.tm_min} 分 {t.tm_sec} 秒')

    def run(self):
        # 获取商家数据
        TorF_display_Merchant = ''

        Merchant_data = self.get_lunch_data()

        TorF_display_Merchant = input('是否显示已经可以报名的商家 (默认不显示,如需显示输入T)')
        if(TorF_display_Merchant == ''):
            Merchant_data = [i for i in Merchant_data if i['status']== 0]
        # 列出清单
        self.display_Merchant_data(Merchant_data)
        
        Merchant_id = int(input("\n选择的商家id:"))
        Merchant_activity_id = Merchant_data[Merchant_id-1]['id']
        Merchant_begin_time = Merchant_data[Merchant_id-1]['beginDate']

        print('已选择商家：{0}\t{1} 开始'.format(Merchant_data[Merchant_id-1]['businessName'],Merchant_begin_time))
        
        self.Grab_tickets(Merchant_begin_time,Merchant_activity_id)
        time.sleep(30)

    def test(self):
        # file = open("data.json",'w+')
        # file.write(json.dumps(self.get_lunch_data(), sort_keys=True, indent=4, separators=(',', ': ')))
        # file.close
        self.Grab_tickets('21:45',283449)

if __name__ == '__main__':
    qiangpiao = bawangcan_Grab_tickets()
    qiangpiao.test()
    # qiangpiao.run()


