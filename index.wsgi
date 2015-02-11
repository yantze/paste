#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random

# web.py
import web
import markdown

import sae
from sae.storage import Bucket

from pygments import highlight
from pygments.formatters import HtmlFormatter
import pygments.lexers

bucket = Bucket('paste')
prefix = time.strftime("%Y%m")
LENID = 4

# qrurl = 'http://chart.apis.google.com/chart?chs=240x240&cht=qr&choe=UTF-8&chl='
# qrurl = 'http://chart.lanbing.org/chart?&cht=qr&chld=|1&chs=240x240&chl='
qrurl = 'http://tool.oschina.net/action/qrcode/generate?output=image%2Fpng&error=Q&type=0&margin=3&size=4&data='
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
    #  document.getElementsByTagName("textarea").item().setAttribute("rows", 34)
    # j cdn : http://code.jquery.com/jquery-1.11.2.min.js
    form = '''
        <form action="{0}" method="POST" accept-charset="UTF-8">
        <button type="submit">生成链接和二维码</button><br>
        <textarea name="{1}" cols="80" rows="3" onclick='document.getElementsByTagName("textarea")[0].setAttribute("rows", 34)'></textarea><input type="hidden" name="qr" value="yes" />
        </form>'''.format(URL, POST)

    return '''
    <style> a {{ text-decoration: none }} </style>
{2}
    <pre>

    PASTE
        放文字和代码的地方

    在命令行中:
        &lt;command&gt; | curl -F '{0}=&lt;-' {1}

    在网页中:
        原文:<a href='{1}/201502aVfY'>{1}/aVfY</a>
        TEXT渲染:<a href='{1}/201502aVfY?text'>{1}/aVfY?text</a>
        markdown渲染:<a href='{1}/201502aVfY?md'>{1}/aVfY?md</a>
        网址后面添加<a href='{1}/201501eRaH?cpp#n-7'>?&lt;lang&gt;</a>支持代码高亮和行数

    例子:
        提交到网站后，可获得类似这里的链接{1}/eRaH?cpp#n-7
        $ cat bin/ching | curl -F '{0}=&lt;-' {1}

    项目说明:
        自然月前的内容,使用长id:{1}/201501eRaH
        eg.URL/201502aVfY, URL/aVfY ,都可以
        网站模仿自:http://sprunge.us
        项目地址:http://github.com/yantze/paste
        联系：yantze@126.com
    </pre>
    '''.format(POST, URL, form, prefix)

def put_blob(data):
    nid = new_id()
    key = dectect_unique_key(nid)
    while  key == False:
        nid = new_id()
        key = dectect_unique_key(nid)
    bucket.put_object(key, data.encode('utf-8'))
    return key

def dectect_unique_key(nid):
    key = 'sae{0}/{1}'.format(prefix, nid)
    # the except dectect the unique key
    try:
        bucket.stat_object(key)
        return
    except Exception as ex:
        return key


class MainHandler():

    def GET(self):
        return '''<html>
        <meta charset="utf-8">
        <body>
        {0}
        </body></html>'''.format(help())

    def POST(self):
        nid = new_id()
        form = web.input()
        data = form.get(POST)
        qrcode = form.get('qr')

        if data:
            key = put_blob(data)
        else:
            return "no data"

        genURL = '{0}/{1}{2}'.format(URL, prefix, key[-LENID:])
        if qrcode:
            img = '<img src="{0}{1}"></img>'.format(qrurl, genURL)
            return '''
            <html>
            <meta charset="utf-8">
            <body>
            {0}<br/>
            生成的链接:<br/>
            {1}
            </body>
            </html>'''.format(img, genURL)
        else:
            return genURL


class ServeHandler():

    def GET(self, id):
        if len(id)>=9:
            key = "sae{0}/{1}".format(id[:6],id[6:])
        else:
            key = "sae{0}/{1}".format(prefix, id)

        try:
            data = bucket.get_object_contents(key)
        except Exception as ex:
            return '{} Not Found'.format(id)


        param = web.input().keys()
        # param[0] is language
        if not param:
            return self.plain(data)
        elif param[0] == 'md':
            try:
                md = u'''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width">
        <title>{0}</title>
        <link rel="stylesheet" href="static/css/{1}.css" type="text/css" media="all" />
    </head>
    <body>
        <article class="markdown-body">
        {2}
        </article>
    </body>
</html>
'''.format(URL, param[0], self.markdown(data))
            except Exception as ex:
                return ex
            return md
        elif param[0] == 'text':
            return '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width">
        <title>{0}</title>
        <link rel="stylesheet" href="static/css/{1}.css" type="text/css" media="all" />
    </head>
    <body>
    <pre>{2}</pre>
    </body>
</html>
'''.format(URL, param[0], self.html(data))
        else:
            return self.syntax(data, param[0])
        # resource = str(urllib.unquoto(resource))

    def plain(self, data):
        web.header("Content-Type","text/plain; charset=utf-8")
        return data

    def html(self, data):
        web.header("Content-Type","text/html; charset=utf-8")
        return data

    def markdown(self, data):
        web.header("Content-Type","text/html; charset=utf-8")
        return markdown.markdown(unicode(data, 'utf8'),
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.abbr',
                'markdown.extensions.attr_list',
                'markdown.extensions.def_list',
                'markdown.extensions.fenced_code',
                'markdown.extensions.footnotes',
                'markdown.extensions.tables',
                'markdown.extensions.smart_strong',
                'markdown.extensions.codehilite',
                'markdown.extensions.meta',
                'markdown.extensions.nl2br',
                'markdown.extensions.sane_lists',
                'markdown.extensions.smarty',
                'markdown.extensions.toc'
            ]
        )


    def syntax(self, data, lang):
        web.header("Content-Type","text/html; charset=utf-8")

        try:
            lexer = pygments.lexers.get_lexer_by_name(lang)
        except:
            lexer = pygments.lexers.TextLexer()

        hl = highlight(
            data,
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

# sae inter py shell
# http://shellpy.sinaapp.com/
