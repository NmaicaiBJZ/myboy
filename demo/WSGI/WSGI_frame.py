def application(env,start_respense):
    start_respense('200 OK' , [('Content-Type','text/html;charset=utf-8')])
    
    file_name = env['PATH_INFO']
    
    if file_name == '/index.py':
        return index()
    elif file_name == '/login.py':
        return login()
    else:
        return 'hello world ！啦啦啦啦啦！'

def index():
    return "这是一个主页"

def login():
    return "这是一个标志"
