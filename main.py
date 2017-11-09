# coding: utf-8

import sys
from flask import Flask
from src.views.index import app as route_index
from src.untils import option

app = Flask(__name__)

def register_route():
    """
    注册蓝图
    :return:
    """
    app.register_blueprint(route_index)


def main():
    register_route()

    port = option.port or 4000
    config = dict(
        host='localhost',
        port=port,
        debug=False,
    )
    app.run(**config)


if __name__ == '__main__':
    main()