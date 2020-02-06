# coding=utf-8

import socket
import re
import multiprocessing


def server_client(sockets):
    
    # 将为客户端服务的套接字设置为非堵塞
    for client_socket in sockets:
        client_socket.setblocking(False)
        try:
            # 如果没有接收到客户端的请求，就会抛出异常
            request = client_socket.recv(1024).decode("utf-8")
        except Exception as err:
            print("没有收到客户端的请求!")
        else:
            if request:
                # 解析request
                #request_list = request.splitlines()
                ## 解析第一行 GET /index.html ... 
                #rep_file = re.match(r"[^/]+(/[^ ]*)", request_list[0]).group(1)
                print(request)
                try:
                    f = open(rep_file, "rb")
                except:
                    response = "HTTP/1.1 404 NOT FOUND\r\n"
                    response += "\r\n"
                    response += "<h>404 NOT FOUND</h>"
                    print(response)
                    client_socket.send(response.encode("utf-8"))
                else:
                    html_content = f.read()
                    f.close()
                    response = "HTTP/1.1 200 OK\r\n"
                    response += "\r\n"
                    response += html_content
                    client_socket.send(response.encode("utf-8"))
                    client_socket.close()
            else:
                sockets.remove(client_socket)
                client_socket.close()
                print("-----客户端请求关闭--------")




def http_server():
    """为浏览器提供服务"""
    # 创建tcp套接字
    http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 保证服务器在先调用close后，资源能被立即释放，防止上次的资源占用端口
    http_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 为其绑定固定的IP和端口号
    SERVER_IP = ""
    PORT = 5543
    http_socket.bind((SERVER_IP, PORT))

    # 将套接字变为监听状态
    http_socket.listen(128)
    # 将套接字设置为非堵塞
    http_socket.setblocking(False)
    client_socket_list = list()

    while True:
        # 循环接受数据
        # 使用主进程来接收客户端链接
        try:
            # 由于http_socket为非堵塞，当没有链接的时候就会抛出异常
            client_socket, clientAddr = http_socket.accept()
            client_socket_list.append(client_socket)
        except:
            continue
        else:
            server_client(client_socket_list)

        # # 使用一个子进程来完成服务
        # server_process = multiprocessing.Process(target=server_client, args=(client_socket,))
        # server_process.start()

        # 由于两个进程中的套接字都指向系统中的同一个FD，
        # 所以需要全部关闭才能开始tcp的4次挥手
        # client_socket.close()
        # client_request = server_client(client_socket)

       
    http_socket.close()


if __name__ == "__main__":
    http_server()
