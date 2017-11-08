
### 基于 Canal 的 MySql RabbitMQ Redis/memcached/mongodb 的nosql同步 （多读、nosql延时不严格 需求）
```
https://github.com/liukelin/canal_mysql_nosql_sync

1.mysql主从配置

2.对mysql binlog(row) parser 这一步交给canal

3.MQ对解析后binlog增量数据的推送

4.对MQ数据的消费（接收+数据解析，考虑消费速度，MQ队列的阻塞）

5.数据写入/修改到nosql （redis的主从/hash分片）

6.保证对应关系的简单性：一个mysql表对应一个 redis实例（redis单线程，多实例保证分流不阻塞），关联关系数据交给接口业务

数据：mysql->binlog->MQ->redis(不过期、关闭RDB、AOF保证读写性能) （nosql数据仅用crontab脚本维护）

请求：http->webserver->redis(有数据)->返回数据 （完全避免用户直接读取mysql）

                    ->redis(无数据)->返回空

7.可将它视为一个触发器，binlog为记录触发事件，canal的作用是将事件实时通知出来，并将binlog解析成了所有语言可读的工具。
在事件传输的各个环节 提高 可用性 和 扩展性 （加入MQ等方法）最终提高系统的稳定。
```


### 传统 Mysql Redis/memcached nosql的缓存 （业务同步） 从cache读取数据->
```
1.对数据在mysql的hash算法分布(db/table/分区)，每个hash为节点（nosql数据全部失效时候，可保证mysql各节点可支持直接读取的性能）

2.mysql主从

3.nosql数据的hash算法分布(多实例、DB)，每个hash为节点

4.nosql数据震荡处理 （当某节点挂了寻找替代节点算法（多层hash替代节点）。。。）

5.恢复节点数据

6.请求：http->webserver->【对key计算一致性hash节点】->connect对应的redis实例
->1.redis(有数据)-> 返回数据

->2.redis(无数据)-> mysql (并写入数据redis) -> 返回数据

->3.redis节点挂掉-> 业务寻址hash替代节点

-> 3.1 redis(有数据) -> 返回数据

-> 3.2 redis(无数据) -> mysql(并写入数据redis) -> 返回数据
```
