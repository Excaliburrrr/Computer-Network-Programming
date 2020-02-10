import pymysql as pym


def main():
    # 创建connection对象
    conn = pym.connect(host='localhost', port=3306, 
            user='root', password='654232', 
            database='JD', charset='utf8') 
    # 获取cursor对象
    cs1 = conn.cursor()

    # 执行select语句，并返回受影响的行数
    count = cs1.execute('select id, name from goods where id>=4')

    # 打印受影响的函数
    print("受影响的行为：%d" %count)

    for i in range(count):
        ret = cs1.fetchone()
        print(ret)

    cs1.close()
    conn.close()


if __name__ == "__main__":
    main()
    

    
