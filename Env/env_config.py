# -*- coding:utf-8 -*-

# 日志、报告、截图 等路径
LOGS_DIR = "/Users/micllo/Documents/works/GitHub/pythonAppium_Android/Logs/"
REPORTS_DIR = "/Users/micllo/Documents/works/GitHub/pythonAppium_Android/Reports/"
SCREENSHOTS_DIR = "/Users/micllo/Documents/works/GitHub/pythonAppium_Android/Screenshots/"

# 服务器地址
SERVER_IP = "127.0.0.1"

# Nginx 端口
NGINX_PORT = "6010"

# Mongo 端口
MONGO_PORT = "27017"

# Nginx中的接口反向代理名称
NGINX_API_PROXY = "api_local"

# 是否启用远程浏览器
REMOTE = False

############################################# 相 同 的 配 置 #############################################

# 邮箱配置参数
ERROR_MAIL_HOST = "smtp.163.com"
ERROR_MAIL_ACCOUNT = "miclloo@163.com"
ERROR_MAIL_PASSWD = "qweasd123"  # 客户端授权密码，非登录密码

# 构建的时候使用前端静态文件路径 ( Api/__init__.py文件的同级目录 ) 'static'、'templates'
GULP_STATIC_PATH = '../Build'
GULP_TEMPLATE_PATH = '../Build/templates'

# 测试报告地址
BASE_REPORT_PATH = "http://" + SERVER_IP + ":" + NGINX_PORT + "/test_report_local/"

# 接口地址( uwsgi )
API_ADDR = SERVER_IP + ":" + NGINX_PORT + "/" + NGINX_API_PROXY

# Selenium Grid Console
# GRID_REMOTE_ADDR = "10.211.55.6:4444"  # win10虚拟机
GRID_REMOTE_ADDR = SERVER_IP + ":5555"  # docker

# mongo 数据库
MONGODB_ADDR = SERVER_IP + ":" + MONGO_PORT
MONGODB_DATABASE = "app_auto_test"

# 报错邮箱地址
MAIL_LIST = ["micllo@126.com"]

# 钉钉通知群
DD_MONITOR_GROUP = "3a2069108f0775762cbbfea363984c9bf59fce5967ada82c78c9fb8df354a624"
DD_AT_PHONES = "13816439135,18717854213"
DD_AT_FXC = "13816439135"
