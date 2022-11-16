'''
2022 © MaoHuPi
lightPyServer/main.py
'''

import os
import sys
import random
import string
import flask

def indexOf(_list:list, item):
    return(_list.index(item) if item in _list else -1)

def dir2index(path):
    parent = '.' if os.path.isfile('./'+os.path.basename(__file__)) else os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
    parent = parent + '/'
    print(path)
    if os.path.isdir(parent + path):
        fileList = os.listdir(parent + path)
        fileList = [fileName for fileName in fileList if (fileName.find('index') > -1 or fileName.find('home') > -1 or fileName.find('main') > -1)]
        path = path + '/' + fileList[0] if len(fileList) > 0 else path
    print(path)
    return(path)

def staticApp():
    app = flask.Flask(__name__)
    path = '.'
    @app.route('/', methods = ['GET', 'POST'])
    def home():
        # print(dir2index('/'))
        return flask.send_from_directory(path, dir2index('./'))
    @app.route("/<path:url>", methods = ['GET', 'POST'])
    def subpage(url):
        # print(dir2index('/' + url))
        return flask.send_from_directory(path, dir2index(url))
    return(app)

def proxyApp():
    app = flask.Flask(__name__, template_folder = './')
    @app.route('/', methods = ['GET', 'POST', 'CONNECT'])
    def home():
        print(flask.request.url)
        return flask.render_template('index.html')
    @app.route("/<path:url>", methods = ['GET', 'POST', 'CONNECT'])
    def subpage(url):
        print(flask.request.url)
        return flask.render_template('home.html')
    return(app)

if __name__ == '__main__':
    args = sys.argv[1:]

    mode = [arg.lower().replace('-', '') for arg in args if arg.find('-') == 0]
    mode = mode[0] if len(mode) > 0 else '-s'

    host = [arg for arg in args if arg.find('.') > -1]
    host = host[0] if len(host) > 0 else '0.0.0.0'

    port = host.split(':')
    port = int(port[1]) if len(port) > 1 else 80

    host = host.split(':')[0]

    if indexOf(['s', 'static', 'server', 'd', 'default'], mode) > -1:
        app = staticApp()
        app.run(host = host, port = port, debug = True)
    if indexOf(['p', 'proxy'], mode) > -1:
        app = proxyApp()
        app.run(host = host, port = port, debug = True)