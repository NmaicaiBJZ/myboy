import re
import socket
import multiprocessing
#注意：使用此程序需要使用当前目录下的html目录里面的html文件
#html文件使用带有超链接的最好，最好可以有图片

def server_client(new_socket):
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
    print(repuest_lines[0])
    ret = re.match(r"[^/]+(/[^ ]*)",repuest_lines[0])
    if ret:
        file_name = ret.group(1)
        
        if file_name == "/":
            file_name = "/index.html"
    print(file_name)

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
        repuest = "HTTP/1.1 200 OK\r\n"
        repuest += "\r\n"
        #发送hender
        new_socket.send(repuest.encode("utf-8"))
        #发送body
        new_socket.send(html_content)

    new_socket.close()


def main():
    tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    tcp_server_socket.bind(('',7890))
    tcp_server_socket.listen(128)
    while True:
        new_socket , cliemt_addr=tcp_server_socket.accept()
        p = multiprocessing.Process(target = server_client, args=(new_socket,))
        p.start()
        new_socket.close()
    tcp_server_socket.close()


if __name__ == '__main__':
    main()
