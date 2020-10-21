from flask import Flask, redirect
from werkzeug.routing import BaseConverter


app = Flask(__name__)

#127.0.0.1:5000/goods/123
#@app.route("/goods/<int:goods_id>") 
@app.route("/goods/<goods_id>")#不加转换器类型，默认是普通字符串的格式（除了/）
def goods_detail(goods_id):#将上面的goods_id传入函数中
    return "goods detail page %s" %goods_id

#自定义转换器2
class MobileConberter(BaseConverter):
    def __init__(self, url_map):
        super(MobileConberter,self),__init__(url_map)
        self.regex = r'1[34578]\d{9}'


#1、定义自己的转换器
class ReqexConverter(BaseConverter):
    def __init__(self, url_map, regex):
        """调用父类的初始化方法"""
        super(ReqexConverter,self).__init__(url_map)
        #将正则表达式的参数保存到对象的属性中，flask会去使用这个属性来进行路由的正则匹配
        self.regex = regex

    def to_python(self, value): 
        print("to_python方法被调用")
        #return "abc"
        #value 是在路径进行正则表达式匹配的时候提取的参数
        return value #to_python 将返回值返回给接收的下面mobile_num的值

    def to_url(self, value):
        #value是下面跳转网页(index)传递的值（mobile_num)
        #return "1233"#127.0.0.1:5000/send/1233
        print("to_url方法被调用")
        return value #返回值给要访问的网址


#2.将自定义的转换器添加到flask应用中
app.url_map.converters["re"] = ReqexConverter
app.url_map.converters["mobile"] = mo

#127.0.0.1:5000/send/18612345678
#@app.route("/send/<re(r'1[34578]\d{9}'):mobile>")

@app.route("/send/<mobile:mobile_num>")
def send_sms(mobile):
    return "send sms to %d" % mobile_num


@app.route("/index")
def indes():
    url = url_for("send_sms", mobile_num="18922222222")
    #/send/18922222222
    return redirect(url) #跳转网址到上面的/send/...中


if __name__ = "__main__":
    print(app.url_map) #通过url_map来查看所有路由
    app.run
