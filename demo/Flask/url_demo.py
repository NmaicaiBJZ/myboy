from flask import Flask, redirect
#调用flask框架,redirect用于重定向


app = Flask(__name__)

@app.route("/") #将路由映射到视图
def index():#定义视图页面
	return "hello Flask"

#通过methods限定访问方式
@app.route("/post_only",methods=["GET","POST"])
def post_only():
	return "POST ONLY Page"

#1、用同一个路由定义多个视图
@app.route("/hello",methods=["POST"]):#如果没有路由的定义，首先使用第一个。
def hello1():
	return "hello1"

@app.route("/hello",methods=["GET"]):
def hello2():
	return "hello2"

#2、用同一个视图定义多个路由
@app.route("/h1")
@app.route("/h2")
def h1():
	return "hi page"

#3、跳转路径,重定向
@app.route("/login")
def login():
	#url = "/"
	#只用url_for 的函数，通过视图函数的名字找到视图对应的url路径
	url = url_for("index")
	return 


if __name__ = "__main__":
	print(app.url_map) #通过url_map来查看所有路由
	app.run()#run有一些参数host:地址，port:端口,debug:开启debug模式
