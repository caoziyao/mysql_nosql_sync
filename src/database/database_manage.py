# coding: utf-8

import pymysql
from config.config import mysql_config

# config = {
#     "host": "127.0.0.1",
#     "port": 3306,
#     "username": "root",
#     "password": "zy123456",
#     "dbname": "test_master",
#     "charset": "utf8"
# }

class DBManager(object):
    _instance = None
    _pool = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DBManager, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        if self._pool is None:
            cf = mysql_config
            self._pool = pymysql.connect(
                host=cf['host'],
                port=cf['port'],
                user=cf['username'],
                password=cf['password'],
                db=cf['dbname'],
                charset=cf['charset'],
                cursorclass=pymysql.cursors.DictCursor,
            )
            print('connect mysql {}'.format(cf['dbname']))

    @property
    def pool(self):
        """
        链接池
        :return:
        """
        return self._pool

    def join_field_value(self, data, glue=', '):
        sql = comma = ''
        for key in data.keys():
            sql += "{}`{}` = %s".format(comma, key)
            comma = glue
        return sql

    def _condition(self, condition):
        prepared = []  # PreparedStatement
        if not condition:
            where = '1';
        elif isinstance(condition, dict):
            where = self.join_field_value(condition, ' AND ')
            prepared.extend(condition.values())
        else:
            where = condition

        return where, prepared

    def _fields(self, fields):
        if not fields:
            fields = '*'
        elif isinstance(fields, (tuple, list)):
            fields = '`, `'.join(fields)
            fields = '`{fields}`'.format(fields=fields)
        else:
            fields = fields

        return fields

    def _order(self, order):
        if not order:
            orderby = ''
        else:
            orderby = 'ORDER BY {order}'.format(order=order)

        return orderby

    def _result_by_sql(self, cursor, sql, prepared):

        if not prepared:
            result = cursor.execute(sql)
        else:
            result = cursor.execute(sql, tuple(prepared))

        return result

    def insert(self, table, data):
        """ mysql insert() function
        user = {'email': 'ringzero@0x557.org', 'password': '123123'}
        dbconn.insert(table='users', data=user)

        # change user dict, 修改用户信息提交
        user['email'] = 'ringzero@wooyun.org'
        user['password'] = '123456'
        dbconn.insert(table='users', data=user)

        'insert ignore into users set `email` = %s, `password` = %s'
        """
        with self.pool.cursor() as cursor:
            params = self.join_field_value(data);
            sql = 'insert ignore into {table} set {params}'.format(table=table, params=params)
            res = cursor.execute(sql, tuple(data.values()))
            self.pool.commit()
            if res:
                rol_id = cursor.lastrowid
            else:
                rol_id = None

            return rol_id

    def delete(self, table, condition=None, limit=None):
        """
        cond = {'email': 'ringzero@0x557.org'}
        rows = dbconn.delete(table='users', condition=cond, limit='1')
        print('deleted {} records success..'.format(rows))
        """
        with self.pool.cursor() as cursor:
            where, prepared = self._condition(condition)

            limits = "LIMIT {limit}".format(limit=limit) if limit else ""
            sql = "DELETE FROM {table} WHERE {where} {limits}".format(
                table=table, where=where, limits=limits)

            result = self._result_by_sql(cursor, sql, prepared)
            self.pool.commit()  # not autocommit

            return result

    def update(self, table, data, condition=None):
        """
        user = {'email': 'newringzero@0x557.org', 'password': '888888'}
        cond = {'email': 'ringzero@0x557.org'}
        rows = dbconn.update(table='users', data=user, condition=cond)
        print('update {} records success..'.format(rows))
        """
        with self.pool.cursor() as cursor:
            prepared = []  # PreparedStatement
            params = self.join_field_value(data)
            prepared.extend(data.values())

            where, pre = self._condition(condition)
            prepared.extend(pre)

            sql = "UPDATE {table} SET {params} WHERE {where}".format(
                table=table, params=params, where=where)

            result = self._result_by_sql(cursor, sql, prepared)

            self.pool.commit()  # not autocommit
            return result

    def count(self, table, condition=None):
        """
        cond = {'email': 'ringzero@wooyun.org'}
        cnt = dbconn.count(
                        table='users',
                        condition=cond)
        print(cnt)
        """
        with self.pool.cursor() as cursor:
            where, prepared = self._condition(condition)

            # SELECT COUNT(*) as cnt
            sql = "SELECT COUNT(*) as cnt FROM {table} WHERE {where}".format(
                table=table, where=where)

            self._result_by_sql(cursor, sql, prepared)

            return cursor.fetchone().get('cnt')

    def fetch_rows(self, table, fields=None, condition=None, order=None, limit=None, fetchone=False):
        """ mysql select() function
        fields = ('id', 'email')
        cond = {'email': 'ringzero@wooyun.org'}
        rows = dbconn.fetch_rows(
            table='users',
            fields=fields,
            condition=cond,
            order='id asc',
            limit='0,5'
        )
        #  SELECT username FROM users WHERE `username` = %s ORDER BY id asc LIMIT 0,5

        for row in rows:
            print(row)

        # 不指定 fields 字段, 将返回所有*字段,
        # 不指定 order, 将不进行排序
        # 不指定 limit, 将返回所有记录

        rows = dbconn.fetch_rows(
            table='users',
            condition=cond,
            limit='0,5'
        )
        for row in rows:
            print(row)
        :param limit:  不指定 limit, 返回全部数据
        """
        with self.pool.cursor() as cursor:

            fields = self._fields(fields)
            where, prepared = self._condition(condition)
            orderby = self._order(order)

            limits = "LIMIT {limit}".format(limit=limit) if limit else ""

            sql = "SELECT {fields} FROM {table} WHERE {where} {orderby} {limits}".format(
                fields=fields, table=table, where=where, orderby=orderby, limits=limits)

            self._result_by_sql(cursor, sql, prepared)

            if fetchone:
                return cursor.fetchone()
            else:
                return cursor.fetchall()

    def query(self, sql, fetchone=False):
        """execute custom sql query
        sql = 'select * from users limit 0, 5'
        rows = dbconn.query(sql)
        for row in rows:
            print(row)
        """
        with self.pool.cursor() as cursor:
            if not sql:
                return None
            cursor.execute(sql)
            self.pool.commit()  # not auto commit
            if fetchone:
                return cursor.fetchone()
            else:
                return cursor.fetchall()


    def __del__(self):
        """close mysql database connection"""
        if self._pool is not None:
            return self._pool.close()

data_manager = DBManager()