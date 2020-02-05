# coding=utf-8

import socket
import re


def server_client(new_socket):

    request = new_socket.recv(1024).decode("utf-8")
    # 解析request
    request_list = request.splitlines()
    # 解析第一行 GET /index.html ... 
    print(request_list[0])
    rep_file = re.match(r"[^/]+(/[^ ]*)", request_list[0]).group(1)
    print(rep_file)

    try:
        f = open(rep_file, "rb")
    except:
        response = "HTTP/1.1 404 NOT FOUND\r\n"
        response += "\r\n"
        response += "<h>404 NOT FOUND</h>"
        print(response)
    else:
        html_content = f.read()
        f.close()
        response = "HTTP/1.1 200 OK\r\n"
        response += "\r\n"
        response += html_content

    if request:
        new_socket.send(response.encode("utf-8"))
        new_socket.close()
        return request
    else:
        return False


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

    while True:
        # 循环接受数据
        client_socket, clientAddr = http_socket.accept()

        # 接收客户端发送的请求
        client_request = server_client(client_socket)
        if client_request:
            print("收到请求信息\n:%s\n" %client_request)
            print("成功发送网页信息！")
        else:
            print("未收到请求，请重新访问")

       
    http_socket.close()


if __name__ == "__main__":
    http_server()
