#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import web
import markdown
import codecs
import os.path

urls = (
    "/(.*\.md)", 'Markdown',
    "/(.*\.md)/raw", 'Raw',
    "/(.*/)?", 'Index',
)

def getMarkdown():
    return markdown.Markdown(extensions=['tables','toc','attr_list','footnotes','meta', 'def_list'])

render = web.template.render(
	os.path.dirname(os.path.abspath(__file__))+'/templates'
)

class Index :
    def GET(self, index_path) :
        if not index_path :
            index_path=""
        return Markdown().GET(index_path+'index.md')

class Raw :
    def GET(self, input_filename) :
        input_file = web.ctx.env['DOCUMENT_ROOT'] + '/' + input_filename
        if not os.path.isfile(input_file) :
            raise web.notfound()
        input_file = codecs.open(input_file, mode="r", encoding="utf-8")
        unicode_content=input_file.read()
        return unicode_content.encode('ascii', 'xmlcharrefreplace')
        

class Markdown :
    def GET(self, input_filename) :
        input_file = web.ctx.env['DOCUMENT_ROOT'] + '/' + input_filename
        if not os.path.isfile(input_file) :
            raise web.notfound()
        input_file = codecs.open(input_file, mode="r", encoding="utf-8")
        unicode_content=input_file.read()
        md_content=unicode_content.encode('ascii', 'xmlcharrefreplace')
        md = getMarkdown()
        content = md.convert(md_content)
        meta = md.Meta
        return render.markdown(content, meta, input_filename+"/raw")


app = web.application(urls, globals())

#markdown_app = app
#mapping = ("/homebrew", markdown_app)
#app=web.subdir_application(mapping)

web.wsgi.runwsgi = lambda func, addr="/tmp/python-markdown-fcgi.sock": web.wsgi.runfcgi(func,addr)

if __name__ == '__main__' :
   app.run()
