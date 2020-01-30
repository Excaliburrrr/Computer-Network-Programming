import socket

def client():
    # 1、创建TCP套接字
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 目标地址和端口号
    serve_ip = input("Please input serve_IP: ")
    while True:
        try:
            serve_port = int(input("Please input serve_Port: "))
            break
        except ValueError:
            print("Input Error, please retry.")
            continue

    # 2、链接服务器
    sever_addr = (serve_ip, serve_port)
    tcp_client_socket.connect(sever_addr)

    # 3、提示用户输入
    send_data = input("Please enter the message to be sent: ")
    # 客户端向服务端发送数据
    tcp_client_socket.send(send_data.encode('utf-8'))

    # 4、接收对方发送过来的消息

    # 5、关闭套接字
    tcp_client_socket.close()

if __name__ == "__main__":
    client()
