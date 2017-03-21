#这里MySQLdb不能用了，新的Django全部用pymysql，连接mysql数据库
import pymysql
pymysql.install_as_MySQLdb()