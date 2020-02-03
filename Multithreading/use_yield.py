import time

"""使用yield实现并发"""

def func1():
    while True:
        print("----1----")
        time.sleep(0.1)
        yield


def func2():
    while True:
        print("----2----")
        time.sleep(0.1)
        yield

def main():
    f1 = func1()
    f2 = func2()
    while True:
        next(f1)
        next(f2)
    

if __name__ == "__main__":
    main()
        
