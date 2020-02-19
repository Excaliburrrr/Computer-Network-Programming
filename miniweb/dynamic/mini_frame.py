import time
from register import *
from util_sql import Stocks
from urllib.parse import unquote
import re
import logging


def get_logger():
    """log日志的设置"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logfile = "./log.txt"
    fh = logging.FileHandler(logfile, mode='a')
    fh.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)

    fomatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(fomatter)
    ch.setFormatter(fomatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


@route(r'/add/(\d+)\.html')
def add(ret):
    logger = get_logger()
    stock = Stocks()
    # 1、获取股票代码
    stock_code = ret.group(1)
    # 2、判断是否有这只股票，一般只有网站被爬的时候会出现
    if not stock.exists(stock_code):
       return "非法操作, 股票不存在!"
    # 3、判断是否关注过
    if stock.is_focus(stock_code):
        return "该股票已关注，请勿再次关注"
    # 4、添加关注
    try:
        stock.add_focus(stock_code)
    except SystemError as ret:
        return ret
    else:
        logger.info("用户关注了 %s 这支股票" %stock_code)
    return "关注成功"


@route(r'/del/(\d+)\.html')
def del_focus(ret):
    logger = get_logger()
    stock = Stocks()
    # 1、获取股票代码
    stock_code = ret.group(1)
    # 2、判断是否关注过，如果没有则是非法请求
    if not stock.is_focus(stock_code):
        return "非法操作，未关注该股票！"
    # 3、取消关注
    try:
        stock.del_focus(stock_code)
    except SystemError as ret:
        return ret
    else:
        logger.info("用户取消了 %s 这支股票" %stock_code)
    return "取消成功"

@route(r'/update/(\d+)\.html')
def show_update_page(ret):
    stock = Stocks()
    # 1. 获取股票代码
    stock_code = ret.group(1)
    # 2. 获取对该股票的备注信息
    note_info = stock.get_note_info(stock_code)
    with open("./templates/update.html", "r") as f:
        content = f.read()

    content = re.sub(r'\{%code%\}', stock_code, content)
    content = re.sub(r'\{%note_info%\}',  note_info, content)
    return content

@route(r'/update/(\d+)/(.*)\.html')
def update_note(ret):
    logger = get_logger()
    stock = Stocks()
    # 1. 获取股票代码, 与提交的备注修改
    stock_code = ret.group(1)
    # 对new_note进行url解码
    new_note = unquote(ret.group(2))
    # 2. 对该股票的备注进行修改
    try:
        stock.update_note(stock_code, new_note)
    except SystemError as ret:
        return ret
    else:
        logger.info("用户为 %s 这支股票添加了备注：%s" %(stock_code, new_note))
    return "修改成功 %s" %new_note

@route(r'/index.html')
def index(ret):
    stock = Stocks()
    stock_infos = stock.get_stock_infos()

    html = ""
    ht_template = """<tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>
            <input type="button" value="添加" id="toAdd" name="toAdd" systemIdValue=%s>
        </td>
    </tr>
    """
    for info in stock_infos:
        html += ht_template %(info.id, info.code, info.short,
            info.chg, info.turnover, info.price, info.highs, info.time, info.code)

    with open("./templates/index.html") as f:
        content = f.read()

    content = re.sub(r'\{%content%\}', html, content)

    return content


@route(r'/center.html')
def center(ret):
    stock = Stocks()
    focus_infos = stock.get_focus_infos()

    html = ""
    ht_template = """<tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>
            <a type="button" class="btn btn-default btn-xs" href="/update/%s.html"> <span class="glyphicon glyphicon-
            star" aria-hidden="true"></span> 修改 </a>
        </td>
        <td>
            <input type="button" value="删除" id="toDel" name="toDel" systemIdValue=%s>
        </td>
    </tr>
    """
    for info in focus_infos:
        html += ht_template %(info.code, info.short, info.chg, info.turnover,
                              info.price, info.highs, info.note_info, info.code, info.code)
    with open("./templates/center.html") as f:
        content = f.read()
    content = re.sub(r'\{%content%\}', html, content)

    return content 


def application(environ, start_response):
    file_name = environ["PATH_INFO"]
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])
    try:
        for url, call_module in URL_MODULE_DICT.items():
            print(url)
            ret = re.match(url, file_name)
            if ret:
                return call_module(ret)
            else:
                continue
        return "请求的url(%s)没有对应的函数进行处理" %file_name
    except Exception as ret:
        return "产生了异常: %s" %ret

