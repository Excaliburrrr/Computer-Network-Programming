# -*- coding: utf-8 -*-
import pymysql as pym


class JD(object):
    def __init__(self):
        """创建与数据库的链接"""
        self.connect = pym.connect(host='localhost', port=3306,
                                    user='root', password='654232',
                                   database='JD', charset='utf8')
        self.csr = self.connect.cursor()
        # 标志用户是否登陆
        self.is_signin = False
        
        
    def __del__(self):
        """关闭连接"""
        self.csr.close()
        self.connect.close()

    def sign_in(self):
        # 当尝试3次登陆失败则退出登陆
        try_times = 0
        while True:
            if try_times == 3:
                print("登陆失败！")
                return 0 
            print("请输入手机号和密码\r")
            customer_tel = input("账号: ")
            customer_passwd = input("密码: ")
            info_list = [customer_tel, customer_passwd]
            self.csr.execute("""SELECT name FROM customers WHERE tel=%s AND passwd=%s""", info_list)
            customer_name = self.csr.fetchone()
            if customer_name:
                print("欢迎光临, %s!" %customer_name[0])
                self.is_signin = True
                # 获取登陆用户的id
                self.csr.execute("""SELECT id FROM customers WHERE tel=%s""", [customer_tel])
                customer_ID = self.csr.fetchone()[0]
                return customer_ID 
            else:
                print("账号或密码错误，请重新输入！")
                try_times += 1


    def log_in(self):
        while True:
            customer_name = input("请输入您的姓名: ").encode("utf-8")
            customer_tel = input("请输入您的手机号: ")
            customer_passwd = input("请输入您的密码(8位): ")
            customer_addr = input("请输入您的收货地址: ").encode("utf-8")
            # 判断该手机号是否注册
            self.csr.execute("""SELECT tel FROM customers WHERE tel=%s""", [customer_tel])
            if self.csr.fetchall():
                print("该手机号已经被注册，请换一个手机号！")
                continue
            else:
                customer_info = [customer_name.decode("utf-8"), customer_addr.decode("utf-8"), customer_tel, customer_passwd]
                self.csr.execute("""INSERT INTO customers VALUES (0, %s, %s, %s, %s)""", customer_info)
                self.connect.commit()
                print("注册成功！")
                self.is_signin = True
                # 获取用户ID并返回
                self.csr.execute("""SELECT id FROM customers where tel=%s""", [customer_tel])
                return self.csr.fetchone()[0]
                

    def enter_jd_market(self):
        # 标志用户在数据库中的ID号，游客ID为0
        customer_id = 0
        while not self.is_signin:
            # 判断是否登陆
            start_num = input("请选择是否登陆或注册, 登陆请输入1, 注册请输入2, 若以游客身份请输入3: ")
            if start_num == '1':
                # 提示用户登陆, 如果登陆失败则返回0, 登陆成功则返回用户ID
                customer_id = self.sign_in()
            elif start_num == '2':
                # 提示用户注册
                customer_id = self.log_in()
            elif start_num == '3':
                break
        return customer_id


    def order(self, customer_id, shopping_cart):
        """下单操作"""
        # 更新订单表
        self.csr.execute("SELECT NOW()")
        order_time = self.csr.fetchone()[0]
        self.csr.execute("INSERT INTO orders VALUES (0, %s, %s)", [order_time, customer_id])
        self.connect.commit()
        # 获取订单ID
        self.csr.execute("SELECT id FROM orders WHERE customer_id=%s and order_date_time=%s", [customer_id, order_time])
        order_id = self.csr.fetchone()[0]
        for item_id in shopping_cart:
            # 判断订单详情表中是否已经含有该商品
            self.csr.execute("""SELECT quantity FROM order_detail WHERE goods_id=%s""", [item_id])
            item_quantity = int(self.csr.fetchone()[0]) if self.csr.fetchone() else 0
            # 判断该商品是否售罄
            self.csr.execute("""SELECT is_saleoff FROM goods WHERE id=%s""", [item_id])
            is_saleoff = self.csr.fetchone()[0]
            if is_saleoff == b'\x00':
                # 若没有售罄按条件更新商品表的is_saleoff信息
                self.csr.execute("UPDATE goods SET is_saleoff=%s WHERE id=%s", [1, item_id])
                # 购买成功后选择更新订单详情表或往订单详情表中插入新的数据
                if item_quantity:
                    self.csr.execute("UPDATE order_detail SET quantity=%s WHERE goods_id=%s", [item_quantity+1, item_id])
                else:
                    self.csr.execute("INSERT INTO order_detail VALUES(0, %s, %s, %s)", [order_id, item_id, 1])
                self.connect.commit()
            else:
                continue
        print("购买完成！")


    def add_to_cart(self):
        """选择商品并加入购物车"""
        shoppint_cart = []
        while True:
            item_id = input("请输入想要购买的商品编号(按q退出购买): ")
            if item_id == 'q':
                break
            if self.can_buy(item_id):
                shoppint_cart.append(item_id)
                print("添加购物车成功!")
            else:
                print("该商品已售罄, 请另选商品")
        return shoppint_cart


    def can_buy(self, item_id):
        """判断商品是否能加入购物车"""
        self.csr.execute("SELECT is_saleoff FROM goods WHERE id=%s", [item_id])
        is_saleoff = self.csr.fetchone()[0] 
        if is_saleoff == b'\x00':
            return True
        else:
            return False


        
    @staticmethod 
    def print_menu():
        print_str = "查询所有商品名称请输入：1\r\n"
        print_str += "查询所有商品种类请输入：2\r\n"
        print_str += "查询所有商品品牌请输入：3\r\n"
        print(print_str)
        
    
    def execute_sql(self, sql):
        self.csr.execute(sql)
        for item in self.csr.fetchall():
            print("编号: %s 项目: %s" %(item[0], item[1]))


    def show_all_goods(self):
        sql = "select id, name from goods"
        self.execute_sql(sql)


    def show_all_cates(self):
        sql = "select id, name from goods_cates"
        self.execute_sql(sql)


    def show_all_brands(self):
        sql = "select id, name from goods_brands"
        self.execute_sql(sql)


    def run(self):
        # 进入JD商城, 并赋予用户ID
        customer_id = self.enter_jd_market()

        while True:
            self.print_menu()
            num = input("请输入想要查询的页面编号(按q键退出): ")
            if num == "1":
                self.show_all_goods()
                print("进入购买页面请选1, 回到首页请选0")
                option = input("请输入您的选择: ")
                if option == '1':
                    # 返回购物车列表
                    shopping_cart = self.add_to_cart()
                    is_order = input("是否下单(yes/no, y/n): ")
                    if is_order == 'yes' or is_order == 'y':
                        self.order(customer_id, shopping_cart)
                    elif is_order == 'no' or is_order == 'n':
                        continue
            elif num == "2":
                self.show_all_cates()
            elif num == "3":
                self.show_all_brands()
            elif num == 'q':
                break
            else:
                print("请输入正确编号")
                continue

def main():
    jd = JD()
    jd.run()


if __name__ == "__main__":
    main()




