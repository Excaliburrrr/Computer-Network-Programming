import socket

def send():
    # 1、创建udp套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 2、准备接收方的地址
    # '192.168.1.103'表示目标ip地址
    # 8080 表示目标端口
    while True:
        dest_addr = ('192.168.2.179', 8080)

        # 3、从键盘获取数据
        send_data = input("请输入要发送的数据：")
        if send_data == 'exit':
            break

        # 4、发送数据到值定的电脑上的指定程序中,
        udp_socket.sendto(send_data.encode("utf-8"), dest_addr)

    # 5、关闭套接字
    udp_socket.close()

def receive():
    # 1、创建套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 2、绑定本地的相关信息，如果一个网络程序不绑定，则系统会随机分配
    local_addr = ('', 7788) # ip地址和端口号，ip一般不用写，表示本机的任何一个ip
    udp_socket.bind(local_addr)
    while True:
        # 3、等待对方发送的数据，并返回到变量recv_data中
        # 变量 recv_data 类型为元组：(b'内容', ('IP地址', 端口号))
        recv_data = udp_socket.recvfrom(1024)  # 1024表示本次接收的最大字节数
        if recv_data[0].decode('gbk') == 'exit':
            break

        # 4、显示接收到的数据
        print(recv_data[0].decode('gbk'))

    # 5、关闭套接字
    udp_socket.close()




if __name__ == "__main__":
    #send()
    receive()