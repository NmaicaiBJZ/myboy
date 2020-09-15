import re

# URL_FUNC_DICT={
#     "/index.py":index,
#     "/center.py":center
# }
URL_FUNC_DICT = dict()

def route(url):
    def set_func(func):
        #URL_FUNC_DICT["./index.py"] = index 用装饰器来装饰字典，不用在加上一个函数的同时给字典加入这个函数的调用
        URL_FUNC_DICT[url] = func
        def call_func(*args, **kwargs):
            return func(*args, **kwargs)
        return call_func
    return set_func


@route("/index.py")
def index():
    with open("./templates/index.html") as f:
        content = f.read()
    my_stock_info = "这是mysql查询出来的数据"
    content = re.sub(r"\{%content%\}",my_stock_info,content)
    return content


@route("/center.py")
def center():
    with open("./templates/center.html") as f:
        content = f.read()
    my_stock_info = "这是mysql查询出来的数据"
    content = re.sub(r"\{%content%\}",my_stock_info,content)
    return content


def application(env,start_respense):
    start_respense('200 OK' , [('Content-Type','text/html;charset=utf-8')])
    
    file_name = env['PATH_INFO']
    
    #if file_name == '/index.py':
    #    return index()
    #elif file_name == '/login.py':
    #    return login()
    #else:
    #    return 'hello world ！啦啦啦啦啦！'

    func = URL_FUNC_DICT[file_name]    
    return func()
