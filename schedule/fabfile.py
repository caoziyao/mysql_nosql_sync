# coding: utf-8

from fabric.api import local, cd, run, env, settings, task, get
from datetime import datetime

"""
1.主从备份
2. mysqldump 备份，lz4 压缩，
3. 同时也备份 master binlog
    查看 /etc/mysql/mysql.conf.d/my.cnf > /var/lib/mysql/mysql-bin.000001
"""

env.hosts = ['10.211.55.3']
env.host_string = '10.211.55.3'
env.port = 22
env.user = 'working'
env.password = '12345678'

# @task
def dupm_test_master():
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    bk_name = 'test_master_dump_{}.sql'.format(now)

    local_dir = '/Users/Shared/github/mysql_nosql_sync/schedule/mysql_backup'
    local_path = '{}/{}'.format(local_dir, bk_name)

    remote_dir = 'mysql_backup'
    remote_path = '{}/{}'.format(remote_dir, bk_name)

    mysql = 'mysqldump -umonty -psome_pass test_master > {}'.format(remote_path)

    run(mysql)
    get(remote_path, local_path)


def dupm_wiki():
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    bk_name = 'wiki_dump_{}.sql'.format(now)

    local_dir = '/Users/Shared/github/mysql_nosql_sync/schedule/mysql_backup'
    local_path = '{}/{}'.format(local_dir, bk_name)

    mysqldump = '/usr/local/mysql/bin/mysqldump'
    mysql = '{} -uroot -pzy123456 wiki > {}'.format(mysqldump, local_path)

    local(mysql)


def main():
    dupm_wiki()


if __name__ == '__main__':
    main()


