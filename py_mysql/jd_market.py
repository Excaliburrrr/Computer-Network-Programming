import pymysql as pym

class JD(object):
    def __init__(self):
        """创建与数据库的链接"""
        self.connect = pym.connect(host='localhost', port=3306,
                                    user='root', password='654232',
                                    database='JD', charset='utf8')
        print("aaaaaaa")
        self.csr = self.connect.cursor()
        
    def __del__(self):
        """关闭连接"""
        self.csr.close()
        self.connect.close()


    @staticmethod 
    def print_menu():
        print_str = "查询商品名称请输入：1\r\n"
        print_str += "查询商品种类请输入：2\r\n"
        print_str += "查询商品品牌请输入：3\r\n"
    
    def execute_sql(self, sql):
        self.csr.execute(sql)
        for item in self.csr.fetchall():
            print(item)


    def show_all_goods(self):
        sql = "select name from goods"
        self.execute_sql(sql)


    def show_all_cates(self):
        sql = "select name from goods_cates"
        self.execute_sql(sql)


    def show_all_brands(self):
        sql = "select name from goods_brands"
        self.execute_sql(sql)


    def run(self):
        while True:
            self.print_menu()
            num = input("请输入想要查询的页面编号: ")
            if num == "1":
                self.show_all_goods()
            elif num == "2":
                self.show_all_cates()
            elif num == "3":
                self.show_all_brands()
            else:
                print("请输入正确编号")
                continue

def main():
    jd = JD()
    jd.run()


if __name__ == "__main__":
    main()




