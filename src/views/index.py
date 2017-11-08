# coding: utf-8

from flask import Blueprint


import json
import os
from flask import render_template, request
from flask.blueprints import Blueprint
from config.constant import static_folder, template_folder
# from .hot_spot import update_views, views_from_cached


app = Blueprint('basis', __name__, static_folder=static_folder, template_folder=template_folder)


@app.route('/', methods=['GET'])
def index():
    """
    页面入口
    :return:
    """
    return render_template('index.html')