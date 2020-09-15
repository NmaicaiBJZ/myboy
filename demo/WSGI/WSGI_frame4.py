import re
from pymysql import * #数据库

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
			

@route("/index.html")
def index():
    with open("./templates/index.html") as f:
        content = f.read()

    # my_stock_info = "这是mysql查询出来的数据"
    # content = re.sub(r"\{%content%\}",my_stock_info,content)

    conn = connect(host='localhost',port=3306,user='root',password='123456',database='student',charset='utf8')
    cs = conn.cursor()
    count = cs.execute('select * from students;')
    stock_infos = cs.fetchall()
    cs.close()
    conn.close()

    tr_template = """<tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>
        <input type="button" value="添加" id="toAdd">
        </td>
        </tr>
    """

    html = ""
    for line_info in stock_infos:
        html += tr_template %(line_info[0],line_info[1],line_info[2])

    content = re.sub(r"\{%content%\}",html,content)

    return content


@route("/center.html")
def center():
    with open("./templates/center.html") as f:
        content = f.read()
    
    conn = connect(host='localhost',port=3306,user='root',password='123456',database='student',charset='utf8')
    cs = conn.cursor()
    count = cs.execute('select i.id,i.name,i.classid,f.note_info from students as i inner join focus as f on i.id=f.info_id;')
    stock_infos = cs.fetchall()
    cs.close()
    conn.close()

    tr_template = """<tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>
        <input type="button" value="修改" id="todefault" >
        </td>
        <td>
        <input type="button" value="删除" id="toDel" >
        </td>
        </tr>
    """

    html = ""
    for line_info in stock_infos:
        html += tr_template %(line_info[0],line_info[1],line_info[2],line_info[3])

    content = re.sub(r"\{%content%\}",html,content)


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
    try:
        # func = URL_FUNC_DICT[file_name]    
        # return func()
        return URL_FUNC_DICT[file_name]() #用于判断异常，这个直接返回
    except Exception as ret:
        return "产生异常：%s" %str(ret)