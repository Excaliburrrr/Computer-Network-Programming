import socket
import threading


class Sendthread(threading.Thread):
    def run(self):
        # 创建一个套接字
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # 输入接收方的IP和端口号
        dest_ip = input("Please input dest_IP: ")
        dest_port = int(input("Please input dest_Port: "))

        while True:
            # 输入待发送的数据
            send_msg = input("Please enter the message to be sent: ")
            if send_msg == "exit":
                break

            # 发送数据
            udp_socket.sendto(send_msg.encode("utf-8"), (dest_ip, dest_port))

        udp_socket.close()


class Recvthread(threading.Thread):
    def run(self):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address = ("", 8081)

        udp_socket.bind(address)

        while True:
            recv_Data, recv_Addre = udp_socket.recvfrom(1024)

            if recv_Data and recv_Data.decode('gbk') != 'exit':
                print("\n[IP:%s Port:%d]: %s" %(recv_Addre[0], recv_Addre[1], recv_Data.decode('gbk')))
            else:
                break
        udp_socket.close()

if __name__ == "__main__":
    send = Sendthread()
    recv = Recvthread()

    send.start()
    recv.start()


