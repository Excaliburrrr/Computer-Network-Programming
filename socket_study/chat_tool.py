import socket

## 实现功能：
## 使用同一个套接字进行收发数据


def chat_tool():
    # 使用同一个套接字进行收发数据
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_addr = ("", 5533)
    udp_socket.bind(local_addr)

    dest_ip = input("请输入目标IP：")

    while True:
        try:
            dest_port = int(input("请输入目标端口："))
            break
        except ValueError:
            print("输入有误，请重新输入符合规则的端口")
            continue
    while True:
        print("--------xxx聊天室--------")
        print("1:发送消息")
        print("2:接收消息")
        print("0:退出")
        op = input("请输入功能: ")
        if op == "1":
            send_data = input("请输入要发送的消息：")
            udp_socket.sendto(send_data.encode("utf-8"), (dest_ip, dest_port))
        elif op == "2":
            # recvfrom 在没有数据到来的时候会阻塞！
            recv_data = udp_socket.recvfrom(1024)
            print('[来自IP:%s Port:%s]: %s' %(recv_data[1][0], recv_data[1][0], recv_data[0].decode('gbk')))
        elif op == "0":
            break
        else:
            print("输入有误，请重新输入")
    udp_socket.close()


if __name__ == "__main__":
    chat_tool()
