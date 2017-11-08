
from flask import Flask
from src.views.index import app as route_index

app = Flask(__name__)

def register_route():
    """
    注册蓝图
    :return:
    """
    app.register_blueprint(route_index)


def main():
    register_route()
    config = dict(
        host='localhost',
        port=4000,
        debug=True,
    )
    app.run(**config)


if __name__ == '__main__':
    main()