# coding: utf-8


from src.untils import option
from src.share import TypeServer

mysql_config = {
    "host": "127.0.0.1",
    "port": 3306,
    "username": "root",
    "password": "zy123456",
    "dbname": "test_master",
    "charset": "utf8"
}
#
# mysql_config = {
#     "host": "10.211.55.3",
#     "port": 3306,
#     "username": "monty",
#     "password": "some_pass",
#     "dbname": "test_master",
#     "charset": "utf8"
# }


# mysql_config = {
#     "host": "127.0.0.1",
#     "port": 3306,
#     "username": "root",
#     "password": "zy123456",
#     "dbname": "test_slave1",
#     "charset": "utf8"
# }


# if option.server == TypeServer.master:
#     mysql_config = {
#         "host": "10.211.55.3",
#         "port": 3306,
#         "username": "monty",
#         "password": "some_pass",
#         "dbname": "test_master",
#         "charset": "utf8"
#     }
# else:
#     mysql_config = {
#         "host": "10.211.55.3",
#         "port": 3306,
#         "username": "monty",
#         "password": "some_pass",
#         "dbname": "test_slave1",
#         "charset": "utf8"
#     }




