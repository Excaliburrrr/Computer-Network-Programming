# coding=utf-8

import socket
import re
import select


def server_client(new_socket, request):

    # 解析request
    request_list = request.splitlines()

    # 解析第一行 GET /index.html ... 
    rep_file = re.match(r"[^/]+(/[^ ]*)", request_list[0]).group(1)

    try:
        f = open(rep_file, "rb")
    except:
        response_body = "<h>404 NOT FOUND</h>"
        response_header = "HTTP/1.1 404 NOT FOUND\r\n"
        response_header += "Content-Length:%d\r\n" %len(response_body)
        response = response_header + "\r\n" + response_body
        response = response.encode("utf-8")
    else:
        html_content = f.read()
        f.close()
        response_body = html_content
        response_header = "HTTP/1.1 200 OK\r\n"
        response_header += "Content-Length:%d\r\n" %len(response_body)
        response = response_header.encode("utf-8") + "\r\n" + response_body

    new_socket.send(response)


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

    # 创建epoll对象
    epl = select.epoll()

    # 将监听套接字的fd注册到epl中
    epl.register(http_socket.fileno(), select.EPOLLIN)

    # fd->socket map
    fd_socket_map = dict()

    while True:

        # 调用epl中的poll方法，该方法默认堵塞，
        # 当系统监听到epl中出现事件通知时，该方法会解堵塞，并返回一个list
        # 返回的list为 [(fd, event),... ]
        fd_event_list = epl.poll()

        for fd, event in fd_event_list:
            if fd == http_socket.fileno():
                client_socket, clientAddr = http_socket.accept()
                epl.register(client_socket.fileno(), select.EPOLLIN)
                fd_socket_map[client_socket.fileno()] = client_socket
                print(fd_socket_map)
            elif event == select.EPOLLIN:
                request = fd_socket_map[fd].recv(1024).decode("utf-8")
                if request:
                    server_client(fd_socket_map[fd], request)
                else:
                    fd_socket_map[fd].close()

                    # 从epl中注销
                    epl.unregister(fd)

                    # 从字典中删除
                    del fd_socket_map[fd]

    http_socket.close()


if __name__ == "__main__":
    http_server()
