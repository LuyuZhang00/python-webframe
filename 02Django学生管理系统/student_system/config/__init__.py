import pymysql
# 为实现版本兼容，此处设置mysqlclient的版本
pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()