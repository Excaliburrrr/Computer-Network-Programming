# coding=utf-8
import threading
from time import sleep, ctime

# 多线程共享全局变量
g_num = 100
nums = [11, 22]

def test1(nums_temp):
    #global g_num
    #g_num += 1
    #num += 1
    nums_temp.append(33)
    #print("------In test1------g_num = %d" %g_num)
    print("------In test1------g_num = %s" %str(nums_temp))


def test2():
    print("------In test2------g_num = %s" %str(nums))


if __name__ == "__main__":
    t1 = threading.Thread(target=test1, args=(nums,))
    t2 = threading.Thread(target=test2)

    t1.start()
    t2.start()
    print("------In main thread------g_num = %d" %g_num)
    print("------In main thread------nums = %s" %str(nums))

