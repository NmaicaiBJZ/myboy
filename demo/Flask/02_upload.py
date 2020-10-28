from flask import Flask, request

app = Flask(__name__)

#127.0.0.1:5000/upload
@app.route("/upload", methods={"GET","POST"})
def upload():
    """表示前端发送过来的数据"""
    file_obj = request.files.get("pic")
    if file_obj is None: #表示没有发送过来文件
        return "未上传文件"

    # #将文件保存到本地
    # #1.创建一个文件
    # f = open("./demo.png","wb")
    # #2.向文件写内容
    # data = file_obj.read()
    # f.write(data)
    # #3.关闭文件
    # f.close()
    # return "上传成功"

    #直接使用上传的文件对象
    file_obj.save("./demo1.png")
    return "上传成功"

if __name__ == '__main__':
    app.run(debug=True)