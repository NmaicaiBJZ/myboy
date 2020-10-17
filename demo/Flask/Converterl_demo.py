from flask import Flask
from werkzeug.routing import BaseConverter


app = Flask(__name__)

#127.0.0.1:5000/goods/123
#@app.route("/goods/<int:goods_id>") 
@app.route("/goods/<goods_id>")#不加转换器类型，默认是普通字符串的格式（除了/）
def goods_detail(goods_id):#将上面的goods_id传入函数中
    return "goods detail page %s" %goods_id

#1、定义自己的转换器
class ReqexConverter(BaseConverter):
    def __init__(self, url_map, regex):
        """调用父类的初始化方法"""
        super(ReqexConverter,self).__init__(url_map)
        #将正则表达式的参数保存到对象的属性中，flask会去使用这个属性来进行路由的正则匹配
        self.regex = regex

#2.将自定义的转换器添加到flask应用中
app.url_map.converters["re"] = ReqexConverter

#127.0.0.1:5000/send/18612345678
@app.route("/send/<re(r'1[34578]\d{9}'):mobile>")
def send_sms(mobile):
    return "send sms to %d" %mobile



if __name__ = "__main__":
    print(app.url_map) #通过url_map来查看所有路由
    app.run