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
def index(ret):
    with open("./templates/index.html") as f:
        content = f.read()

    # my_stock_info = "这是mysql查询出来的数据"
    # content = re.sub(r"\{%content%\}",my_stock_info,content)

    conn = connect(host='localhost',port=3306,user='root',password='123456',database='student',charset='utf8')
    cs = conn.cursor()
    cs.execute('select * from students;')
    stock_infos = cs.fetchall()
    cs.close()
    conn.close()

    tr_template = """<tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>
        <input type="button" value="添加" id="toAdd" systemidvalue="%s">
        </td>
        </tr>
    """

    html = ""
    for line_info in stock_infos:
        html += tr_template %(line_info[0],line_info[1],line_info[2],line_info[0])

    content = re.sub(r"\{%content%\}",html,content)

    return content


@route("/center.html")
def center(ret):
    with open("./templates/center.html") as f:
        content = f.read()
    
    conn = connect(host='localhost',port=3306,user='root',password='123456',database='student',charset='utf8')
    cs = conn.cursor()
    cs.execute('select i.id,i.name,i.classid,f.note_info from students as i inner join focus as f on i.id=f.info_id;')
    stock_infos = cs.fetchall()
    cs.close()
    conn.close()

    tr_template = """<tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>
        <a type="button" class="btn-a" href="/update/%s.html">修改</a>
        </td>
        <td>
        <input type="button" value="删除" id="toDel" systemidvalue="%s">
        </td>
        </tr>
    """

    html = ""
    for line_info in stock_infos:
        html += tr_template %(line_info[0],line_info[1],line_info[2],line_info[3],line_info[0],line_info[0])

    content = re.sub(r"\{%content%\}",html,content)


    return content


@route(r"/add/(\d+)\.html") #装饰器。。{/app/0000007.html:app_focus,}
def  app_focus(ret):
    #将id,(\d+)输入变量中
    stock_code = ret.group(1)

    conn = connect(host='localhost',port=3306,user='root',password='123456',database='student',charset='utf8')
    cs = conn.cursor()
    sql = """select * from students where id=%s;"""
    cs.execute(sql, (stock_code,))  #防止sql注入，，，
    #如果没有这个id，那么就认为是非法的请求
    if not cs.fetchone(): 
        cs.close()
        conn.close()
        return "没有这个id，大哥我们无冤无仇，请收下留情。。"

    #判断以下是否关注过了
    sql = """select * from students as i inner join focus as f on i.id=f.info_id where i.id=%s;"""
    cs.execute(sql, (stock_code,))
    #如果查出来了，说明已经关注了
    if cs.fetchone():
        cs.close()
        conn.close()
        return "已经关注过了"
    #添加关注
    sql = """insert into focus (info_id) select id from students where id=%s;"""
    cs.execute(sql,(stock_code,))
    conn.commit()
    cs.close()
    conn.close()
    return "关注成功"


@route(r"/del/(\d+)\.html")
def  del_focus(ret):
    stock_code = ret.group(1)

    conn = connect(host='localhost',port=3306,user='root',password='123456',database='student',charset='utf8')
    cs = conn.cursor()
    sql = """select * from students where id=%s;"""
    cs.execute(sql, (stock_code,))  #防止sql注入，，，
    #如果没有这个id，那么就认为是非法的请求
    if not cs.fetchone(): 
        cs.close()
        conn.close()
        return "没有这个id，大哥我们无冤无仇，请收下留情。。"

    #判断以下是否关注过了
    sql = """select * from students as i inner join focus as f on i.id=f.info_id where i.id=%s;"""
    cs.execute(sql, (stock_code,))
    #如果查出来了，说明已经关注了
    if not cs.fetchone():
        cs.close()
        conn.close()
        return "没有关注过"
    #添加关注
    sql = """delete from focus where info_id = (select id from students where id=%s);"""
    cs.execute(sql,(stock_code,))
    conn.commit()
    cs.close()
    conn.close()
    return "取消成功！"


@route(r"/update/(\d+)\.html")
def show_update_page(ret):
    #显示修改的页面
    #获取
    stock_code = ret.group(1)
    #打开模板
    with open("./templates/update.html") as f:
        content = f.read()
    
    conn = connect(host='localhost',port=3306,user='root',password='123456',database='student',charset='utf8')
    cs = conn.cursor()
    sql = """select f.note_info from focus as f inner join students as i on i.id=f.info_id where i.id=%s;"""
    cs.execute(sql,(stock_code,))
    stock_infos = cs.fetchone()
    note_info = stock_infos[0]
    cs.close()
    conn.close()

    content = re.sub(r"\{%note_into%\}",note_info,content)
    content = re.sub(r"\{%code%\}",stock_code,content)

    return content


@route(r"/update/(\d+)/(.*)\.html")
def save_update_page(ret):
    #保存修改的信息
    #获取信息
    stock_code = ret.group(1)
    comment = ret.group(2)
    comment = urllib.parse.unquote(comment)
    
    conn = connect(host='localhost',port=3306,user='root',password='123456',database='student',charset='utf8')
    cs = conn.cursor()
    sql = """update focus set note_info=%s where info_id=(select id from students where id=%s);"""
    cs.execute(sql,(comment,stock_code))
    conn.commit() #确认提交，如果不提交sql不会修改
    cs.close()
    conn.close()

    return """获取成功"""


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
        #return URL_FUNC_DICT[file_name]() #用于判断异常，这个直接返回
        for url, func in URL_FUNC_DICT.items():
            # {
            # r"/index.html":index,
            # r"/center.html":center,
            # r"/add/\d+\.html":add_focus
            # }
            ret = re.match(url, file_name)
            if ret:             #判断ret是否为空，为空调用func引用的函数
                return func(ret)
        else:
            return "请求的url(%s)没有对应的函数。。。" %file_name
    except Exception as ret:
        return "产生异常：%s" %str(ret)