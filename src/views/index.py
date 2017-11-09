# coding: utf-8

from flask import Blueprint


import json
import os
from flask import render_template, request
from flask.blueprints import Blueprint
from config.constant import static_folder, template_folder
# from .hot_spot import update_views, views_from_cached
from src.database import data_manager

app = Blueprint('basis', __name__, static_folder=static_folder, template_folder=template_folder)


@app.route('/', methods=['GET'])
def index():
    """
    页面入口
    :return:
    """
    return render_template('index.html')


# api
@app.route('/api/test_write', methods=['GET'])
def test_write():
    """
    页面入口
    :return:
    """
    manager = data_manager
    data = {
        'username': 'zxc'
    }
    r = manager.insert('tb_user', data)


    # sql = 'insert into test_slave1.tb_user select distinct * from  test_master.tb_user'
    # manager.execute(sql)

    return 'a'


@app.route('/api/test_read', methods=['GET'])
def test_read():
    """
    页面入口
    :return:
    """
    manager = data_manager
    d = manager.fetch_rows('tb_user')

    return json.dumps(d)