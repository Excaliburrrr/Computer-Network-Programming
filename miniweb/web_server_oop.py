# !-*- coding:utf-8 -*- 
import socket
import re
import multiprocessing
import argparse
import sys



class WSGI(object):
    """面向对象的简单web服务器"""
    def __init__(self):
        self.args = self.parse_args()
        # 创建tcp套接字
        self.http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 保证服务器在先调用close后，资源能被立即释放，防止上次的资源占用端口
        self.http_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 为其绑定固定的IP和端口号
        SERVER_IP = ""
        PORT = self.args.port
        self.http_socket.bind((SERVER_IP, PORT))

        # 导入服务器的配置文件
        with open(self.args.config) as f:
            self.cfg = eval(f.read())
        self.dynamic_path = self.cfg['dynamic_path']
        self.static_path= self.cfg['static_path']

        # 导入使用的web框架
        sys.path.append(self.dynamic_path)
        self.frame = __import__(self.args.web_frame)
        self.application = getattr(self.frame, 'application')

        # 将套接字变为监听状态
        self.http_socket.listen(128)

    def __del__(self):
        """服务器停止时，关闭套接字"""
        self.http_socket.close()

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--port", type=int, help="设置服务器端口", default=5543)
        parser.add_argument("-f", "--web_frame", type=str, help="选择使用的web框架", default="mini_frame")
        parser.add_argument("-cfg", "--config", type=str, help="选择服务器的配置", default="./config/web_server.cnf")
        args = parser.parse_args()
        return args

    def server_client(self, new_socket):
        """为客户端提供服务"""
        request = new_socket.recv(1024).decode("utf-8")
        # 解析request
        request_list = request.splitlines()
        # 使用正则解析第一行 GET /index.html ...
        # 匹配出的结果为 '/' 到第二个空格前的内容(包括'/')
        rep_file = re.match(r"[^/]+(/[^ ]*)", request_list[0]).group(1)
        # 在终端显示收到的请求
        print(request)
        if not rep_file.endswith(".html"):
            try:
                f = open(self.static_path + rep_file, "r")
            except:
                response = "HTTP/1.1 404 NOT FOUND\r\n"
                response += "\r\n"
                response += "<h>404 NOT FOUND</h>"
            else:
                html_content = f.read()
                f.close()
                response = "HTTP/1.1 200 OK\r\n"
                response += "\r\n"
                response += html_content
        else:
            # 设定一个字典用于保存浏览器的动态请求信息
            env = dict()
            env["PATH_INFO"] = rep_file
            body = self.application(env, self.set_header)
            header = "HTTP/1.1 %s\r\n" % self.status
            for item in self.headers:
                header += "%s:%s\r\n" % (item[0], item[1])
            header += "\r\n"
            response = header + body

        new_socket.send(response.encode("utf-8"))

        new_socket.close()

    def set_header(self, status, headers):
        self.status = status
        self.headers = [("server", "mini_server v1.0")]
        self.headers += headers

    def run(self):
        """启动web服务器"""
        while True:
            # 循环接受数据
            # 使用主进程来接收客户端链接
            client_socket, clientAddr = self.http_socket.accept()

            # 使用一个子进程来完成服务
            server_process = multiprocessing.Process(target=self.server_client, args=(client_socket,))
            server_process.start()

            # 由于两个进程中的套接字都指向系统中的同一个FD，
            # 所以需要全部关闭才能开始tcp的4次挥手
            client_socket.close()


def main():
    web_server = WSGI()
    web_server.run()


if __name__ == "__main__":
    main()

