# coding: utf-8


from src.untils import option
from src.share import TypeServer

if option.server == TypeServer.master:
    mysql_config = {
        "host": "127.0.0.1",
        "port": 3306,
        "username": "root",
        "password": "zy123456",
        "dbname": "test_master",
        "charset": "utf8"
    }
else:
    mysql_config = {
        "host": "127.0.0.1",
        "port": 3306,
        "username": "root",
        "password": "zy123456",
        "dbname": "test_slave1",
        "charset": "utf8"
    }


