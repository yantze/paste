# -*- coding: utf-8 -*-
import time
import random

# web.py
import web

import sae
from sae.storage import Bucket

from pygments import highlight
from pygments.formatters import HtmlFormatter
import pygments.lexers

bucket = Bucket('paste')
prefix = time.strftime("%Y%m/")
LENID = 4

URL = 'http://paste.sinaapp.com'
POST = 'p'

count = 1

def new_id():
    nid = ''
    symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    while len(nid) < LENID:
        n = random.randint(0, 35)
        nid = nid + symbols[n:n+1]
    return nid

def help():
    form = '''
        data:text/html,<form action="{0}" method="POST" accept-charset="UTF-8">
        <textarea name="{1}" cols="80" rows="24"></textarea>
        <br><button type="submit">{1}</button></form>'''.format(URL, POST)

    return '''
    <style> a {{ text-decoration: none }} </style>
    <pre>

    PASTE

    在命令行中:
        &lt;command&gt; | curl -F '{0}=&lt;-' {1}

    在网页中:
        在网页后面添加<a href='{3}'>?&lt;lang&gt;</a>代码高亮和行数
        用这个<a href='{2}'>链接</a>直接从浏览器复制到网站中

    例子:
        ~$ cat bin/ching | curl -F '{0}=&lt;-' {1}
           {1}/aXZI
        ~$ firefox {1}/aXZI?py#n-7

    项目说明:
        暂时只能放文字
        网站模仿自:http://sprunge.us
        项目地址:  http://github.com/yantze/paste
    </pre>
    '''.format(POST, URL, form, 'http://pygments.org/docs/lexers/')

def put_blob(data):
    nid = new_id()
    key = dectect_unique_key(nid)
    while  key == False:
        nid = new_id()
        key = dectect_unique_key(nid)
    bucket.put_object(key, data.encode('utf-8'))
    return key

def dectect_unique_key(nid):
    key = 'sae{0}{1}'.format(prefix, nid)
    # the except dectect the unique key
    try:
        bucket.stat_object(key)
        return
    except Exception as ex:
        return key

# todo for archive
class ArchiveHandler():
    def GET(self):
        # date = web.input().get('date')
        # if not date:
        #     key = "sae{0}{1}".format(prefix, id)
        # else:
        #     key = "sae{0}{1}".format(date, id)
        return key

class MainHandler():
    def GET(self):
        return '''
        <html>
        <body>
        {0}
        </body>
        </html>
        '''.format(help())

    def POST(self):
        nid = new_id()
        form = web.input()
        data = form.get(POST)
        try:
            key = put_blob(data)
        except Exception as ex:
            return ex
        return '{0}/{1}'.format(URL, key[-LENID:])


class ServeHandler():

    def GET(self, id):
        key = "sae{0}{1}".format(prefix, id)

        try:
            data = bucket.get_object_contents(key)
        except Exception as ex:
            return '{} Not Found'.format(id)


        param = web.input().keys()
        # param[0] is language
        if param:
            return self.html(data, param[0])
        else:
            return self.plain(data)
        # resource = str(urllib.unquoto(resource))

    def plain(self, data):
        web.header("Content-Type","text/plain; charset=utf-8")
        self.data = data
        return self.data

    def html(self, data, lang):
        web.header("Content-Type","text/html; charset=utf-8")
        web.header("viewport","initial-scale=1.0,user-scalable=no,maximum-scale=1,width=device-width")
        self.data = data
        self.lang = lang

        try:
            lexer = pygments.lexers.get_lexer_by_name(lang)
        except:
            lexer = pygments.lexers.TextLexer()

        hl = highlight(
            self.data,
            lexer,
            HtmlFormatter(
                full=True,
                style='perldoc',
                lineanchors='n',
                linenos='inline',
                encoding='UTF-8' # weird, but this works and utf-8 does not.
            )
        )
        return hl

urls = (
        '/',MainHandler,
        '/([^/]+)?', ServeHandler,
        )

# entries
app = web.application(urls, globals()).wsgifunc()
application = sae.create_wsgi_app(app)
