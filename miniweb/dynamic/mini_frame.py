import time
from register import *
import re
import pymysql as pym



@route('/index.html')
def index():
    cnet = pym.connect(host='localhost', port=3306, user='root',
                       password='654232', database='stock_db', charset='utf8')
    cusr = cnet.cursor()
    cusr.execute("SELECT * FROM info;")
    stock_infos = cusr.fetchall()
    cusr.close()
    cnet.close()

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
            <input type="button" value="添加" id="toAdd" name="toAdd" systemidvalue="000007">
        </td>
    </tr>
    """
    for info in stock_infos:
        html += ht_template %(info[0], info[1], info[2],
            info[3], info[4], info[5], info[6], info[7])

    with open("./templates/index.html") as f:
        content = f.read()

    content = re.sub(r'\{%content%\}', html, content)

    return content


@route('/center.html')
def center():
    cnet = pym.connect(host='localhost', port=3306, user='root',
                       password='654232', database='stock_db', charset='utf8')
    cusr = cnet.cursor()
    cusr.execute("""SELECT
                 i.code, i.short, i.chg, i.turnover,
                 i.price, i.highs, f.note_info 
                 FROM focus AS f
                 LEFT JOIN info AS i 
                 ON i.id = f.info_id;""")
    focus_infos = cusr.fetchall()
    cusr.close()
    cnet.close()

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
            <a type="button" class="btn btn-default btn-xs" href="/update/300268.html"> <span class="glyphicon glyphicon-
            star" aria-hidden="true"></span> 修改 </a>
        </td>
        <td>
            <input type="button" value="删除" id="toDel" name="toDel" systemidvalue="300268">
        </td>
    </tr>
    """
    for info in focus_infos:
        html += ht_template %(info[0], info[1], info[2], info[3],
                              info[4], info[5], info[6])
    with open("./templates/center.html") as f:
        content = f.read()
    content = re.sub(r'\{%content%\}', html, content)

    return content 


def application(environ, start_response):
    file_name = environ["PATH_INFO"]
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])
    try:
        return URL_MODULE_DICT[file_name]()
    except Exception as ret:
        return "产生了异常: %s" %ret

