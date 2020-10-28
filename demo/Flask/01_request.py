from flask import Flask

app = Flask(__name__)


#127.0.0.1/index?city=xuancheng #问号后面的是查询参数
@app.route("/index", methods={"GET","POST"})
def index():
    #request中包含了前段发送过来的所有数据
    #form与data是用来提取请求的数据
    #通过request.form可以直接提取请求体中的表单格式的数据，是一个字典的对象
    #通过get方法只能拿到多个同名参数的第一个
    name = request.form.get("name")
    age = request.form.get("age")
    print("request.data: %s" % request.data) 
    name_li = request.form.getlist("name") #getlist可以拿到过个参数

    #args是用来提取url中的参数（查询参数）
    city = request.args.get("city")

    return "hello name=%s, age=%s, city=%s, name_li" % (name, age, city, name_li)

if __name__ == '__main__':
    app.run(debug=True)
