from flask import Flask
#调用flask框架
app = Flask(__name__,
			static_url_path="static",#访问静态的url前缀，默认使用static：port/static/...
			static_folder = "static",#静态文件的目录，默认static
			static_folder = "template"#模板文件的目录，默认template
			)


#使用目录下的配置文件
#1、使用文件配置
#app.config.from_pyfile("config.cfg")#改写法将去寻找主目录下的配置文件
#2、使用对象进行配置
#class config(object):
#	DEBUG = True
#app.config.from_object(config)
#3、直接配置文件
app.config["DEBUG"] = True


app.route("/") #将路由映射到视图
def index():#定义视图页面
	return "hello Flask"

if __name__ = "__main__":
	app.run()#run有一些参数host:地址，port:端口,debug:开启debug模式
