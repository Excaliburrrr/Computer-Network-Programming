# coding=utf-8

import socket
import re
import multiprocessing


def server_client(new_socket, request):
    
    ## 尝试接收客户端发来的请求
    #try:
    #    request = new_socket.recv(1024).decode("utf-8")
    ## 如果没有接收到客户端的请求，就会抛出异常
    #except Exception as err:
    #    print("没有收到客户端的请求!")
    #    return 
    #else:
    # 解析request
    request_list = request.splitlines()
    # 解析第一行 GET /index.html ... 
    rep_file = re.match(r"[^/]+(/[^ ]*)", request_list[0]).group(1)
    try:
        f = open(rep_file, "rb")
    except:
        response = "HTTP/1.1 404 NOT FOUND\r\n"
        response += "Content-Length:4\r\n"
        response += "\r\n"
        response += "hhhh"
        new_socket.send(response.encode("utf-8"))
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
    # 将套接字设置为非堵塞
    http_socket.setblocking(False)
    client_socket_list = list()

    while True:
        # 循环接受数据
        # 使用主进程来接收客户端链接
        try:
            # 由于http_socket为非堵塞，当没有链接的时候就会抛出异常
            client_socket, clientAddr = http_socket.accept()
        except:
            pass
        else:
            client_socket.setblocking(False)
            client_socket_list.append(client_socket)
    
        for new_socket in client_socket_list:
            try:
                request = new_socket.recv(1024).decode("utf-8")
            except Exception as ret:
                pass
            else:
                if request:
                    server_client(new_socket, request)
                else:
                    client_socket_list.remove(new_socket)
                    new_socket.close()



        
        
        
    #server_client(new_socket)




       
    http_socket.close()


if __name__ == "__main__":
    http_server()
