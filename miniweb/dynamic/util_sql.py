from sqlalchemy import Column, VARCHAR, Integer, ForeignKey, create_engine, DATE
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 创建数据表
class Info(Base):
    __tablename__ = 'info'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, default=None)
    code = Column(VARCHAR(6), nullable=True, default=None)
    short = Column(VARCHAR(10), nullable=True, default=None)
    chg = Column(VARCHAR(10), nullable=True, default=None)
    turnover= Column(VARCHAR(255), nullable=True, default=None)
    price = Column(VARCHAR(10, 2), nullable=True, default=None)
    highs = Column(VARCHAR(10, 2), nullable=True, default=None)
    time = Column(DATE, nullable=False, default=None)


class Focus(Base):
    __tablename__ = 'focus'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, default=None)
    note_info = Column(VARCHAR(200), nullable=True, default=None)
    info_id = Column(Integer, ForeignKey("info.id"), nullable=True, default=None)


"""该模块封装Stocks数据库的相关操作"""
class Stocks():
    def __init__(self):
        # 创建DBsession链接类型
        # 创建链接
        engine = create_engine('mysql+pymysql://root:654232@localhost:3306/stock_db', max_overflow=5)

        DBsession = sessionmaker(bind=engine)
        self.session = DBsession()

    def __del__(self):
        self.session.close()

    def get_stock_infos(self):
        """得到所有股票信息表"""
        stock_infos= self.session.query(Info).all()
        return stock_infos

    def get_focus_infos(self):
        """得到用户关注的股票信息"""
        focus_infos = self.session.query(Info.code, Info.short, Info.chg, Info.turnover,
                           Info.price, Info.highs, Focus.note_info).join(Focus, Focus.info_id==Info.id)
        return focus_infos

    def get_note_info(self, code):
        """获取用户对指定股票的备注信息"""
        try:
            note_info = self.session.query(Focus.note_info)\
                .join(Info, Info.id==Focus.info_id).filter(Info.code==code).all()
        except Exception as ret:
            return ret
        return note_info[0].note_info

    def exists(self, code):
        """判断股票是否存在"""
        stock_info = self.session.query(Info).filter(Info.code==code).all()
        if stock_info:
            return True
        else:
            return False

    def is_focus(self, code):
        """判断股票是否已经被关注"""
        focus_info = self.session.query(Info)\
            .join(Focus, Focus.info_id==Info.id).filter(Info.code==code).all()
        if focus_info:
            return True
        else:
            return False

    def add_focus(self, code):
        """添加关注"""
        try:
            stock_info = self.session.query(Info).filter(Info.code == code).all()[0]
        except Exception:
            raise SystemError("系统错误，添加失败！")
        else:
            self.session.add(Focus(info_id=stock_info.id, note_info=""))
            self.session.commit()

    def del_focus(self, code):
        """取消关注"""
        try:
            stock_info = self.session.query(Info).filter(Info.code == code).all()[0]
        except:
            raise SystemError("系统错误，删除失败！")
        else:
            self.session.query(Focus).filter(Focus.info_id==stock_info.id).delete()
            self.session.commit()


    def update_note(self, code, note):
        """对指定的股票的备注进行修改"""
        try:
            stock_info = self.session.query(Info).filter(Info.code == code).all()[0]
        except:
            raise SystemError("系统错误，修改失败")
        else:
            self.session.query(Focus)\
                .filter(Focus.info_id==stock_info.id).update({Focus.note_info:note})
            self.session.commit()


