from flask import Flask, request

app = Flask(__name__)

@app.route("/login", methods={"GET","POST"})
def login():
	#name = request.form.get()
	#pwd = requset.form.get()
	name = ""
	pwd = ""
	if name != "zhangsan" or pwd != "admin":
		#使用abort函数可以立即终止视图函数的执行
		#并可以返回前端特定的信息
		#1、传递状态信息，必须是标准的http状态码:400.404.500.
		abort(400)
		#2、传递响应信息
		resp = Response("login faild ")
		abort(resp)

	return "login success!"



if __name__ == '__main__':
    app.run(debug=True)