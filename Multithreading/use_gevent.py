from gevent import monkey
import gevent
import time
import random

# 将所有非gevent中的延时操作替换为gevent中的延时操作
monkey.patch_all()


def func1(work_name):
    while True:
        print("---%s---" %work_name)
        time.sleep(random.random() * 2)


gevent.joinall([
    gevent.spawn(func1, "work1"),
    gevent.spawn(func1, "work2")
])
        

