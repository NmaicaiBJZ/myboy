import re
import socket
import WSGI_frame

#注意：使用此程序需要使用当前目录下的html目录里面的html文件
#html文件使用带有超链接的最好，最好可以有图片
class WSGI_mini_web(object):
    def __init__(self):
       self.tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
       self.tcp_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
       self.tcp_server_socket.bind(('',7890))
       self.tcp_server_socket.listen(128)


    def server_client(self,new_socket):
        """为客户端返回数据"""
        #接收发送过来的数据
        repuest = new_socket.recv(1024).decode("utf-8")
        repuest_lines = repuest.splitlines() # 将数据转弯为列表
        print("")
        print(">" * 10)
        #将数据答应到控制台
        print(repuest_lines)

        #为客户端返回数据
        file_name = ""
        """数据接收到  get /.... 1.1 ...
                正则表达式匹配该文件的地址"""
        ret = re.match(r"[^/]+([^ ]*)",repuest_lines[0])
        if ret:
            file_name = ret.group(1)
            if file_name == "/":
                file_name = "/index.html"

        if not file_name.endswith(".py"):
        #排除异常
            try:
                f=open("./html"+file_name,"rb")
            except:
                repuest = "HTTP/1.1 404 NOT FOUND\r\n"  # 返回表头
                repuest += "\r\n"
                repuest += "------file not found---------"
                new_socket.send(repuest.encode("utf-8"))
            else:
                html_content = f.read()
                f.close()
                repuest = "HTML/1.1 200 OK"
                repuest += "\r\n"
                #发送hender
                new_socket.send(repuest.encode("utf-8"))
                #发送body
                new_socket.send(html_content)
        else:
            #如果是以.py结尾的则认为是动态请求
            env = dict()
            #将数据处理传送到框架上来返回报文头与底
            #报文头由set_response_header处理
            #身体由函数返回

            #字典是传入需要处理的数据
            env['PATH_INFO'] = file_name

            body = WSGI_frame.application(env, self.set_response_header)

            header = "HTTP/1.1 %s\r\n" % self.status

            for temp in self.headers:
                header += "%s:%s\r\n" % (temp[0],temp[1])

            header += "\r\n"

            response = header + body 

            new_socket.send(response.encode("utf-8"))

        new_socket.close()

    def set_response_header(self,status,headers):
        self.status = status
        self.headers = headers

    def run(self):
       while True:
           new_socket , cliemt_addr=self.tcp_server_socket.accept()
           self.server_client(new_socket)


def main():
    web = WSGI_mini_web()
    web.run()

if __name__ == '__main__':
    main()
