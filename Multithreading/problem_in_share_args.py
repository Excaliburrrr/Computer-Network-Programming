import threading
import time


g_num = 0
mutex = threading.Lock()

def add_1(times, thread_num):

    global g_num
    for i in range(times):
        mutex.acquire()
        g_num += 1
        mutex.release()
    print("-----%s------g_num = %d" %(thread_num, g_num))


def test1():
    t1 = threading.Thread(target=add_1, args=(1000000, "thread1"))
    t2 = threading.Thread(target=add_1, args=(1000000, "thread2"))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print("g_num = %d" %g_num)


if __name__ == "__main__":
    test1()
