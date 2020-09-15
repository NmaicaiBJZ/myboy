import socket

tcp_sev_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcp_sev_socket.bind(("",7890))
tcp_sev_socket.listen(128)
print("等待链接")
new_socket,new_adder=tcp_sev_socket.accept()
print("链接成功，等待接收。。。")
socket_data=new_socket.recv(1024)
print(new_adder)
print(socket_data.decode("utf-8"))
new_socket.seed("123".encode("utf-8"))
new_socket.close()

tcp_sev_socket.close()
