import time
import threading


# 继承Thread类来定义自己的线程类
class Mythread(threading.Thread):
    def run(self):
        for i in range(5):
            time.sleep(1)
            msg = "I'm " + self.name + " @ " + str(i)
            print(msg)






def main():
    for i in range(3):
        t = Mythread()
        t.start()


if __name__ == "__main__":
    main()
