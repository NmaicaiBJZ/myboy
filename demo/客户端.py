import socket


def main():
    #创建套接字
    tcp_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #链接服务器
    tcp_socket.connect(("192.168.19.1",7788))
    #发送数据
    seed_data=input("请输入要要发送的数据:")
    tcp_socket.send(seed_data.encode("utf-8"))
    #接受数据
    recvData=tcp_socket.recv(1024)
    print(recvData.decode("utf-8"))
    #关闭客户端
    tcp_socket.close()

if __name__=="__main__":
    main()
