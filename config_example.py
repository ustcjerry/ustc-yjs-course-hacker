# -*- coding: utf-8 -*-

enable_mail = True  # 此行表示是否发送邮件提醒，设置为 True 发邮件
smtp_server = 'mail.ustc.edu.cn'  # 此行表示 smtp 服务器地址
smtp_username = 'xxx@mail.ustc.edu.cn'  # 此行表示发件人邮箱地址
smtp_password = ''  # 此行表示发件人邮箱密码
smtp_to = 'xxx@xxx.com'  # 此行表示收件人邮箱地址
smtp_ssl = True  # 此行表示连接邮箱是否使用 SSL

student_no = ''  # 此行表示登录教务系统所用学号
ustcmis_password = ''  # 此行表示统一身份验证密码（不是教务系统密码）

req_timeout = 5  # 此行表示向教务系统发查询请求的超时时间（单位：秒）
interval = 30  # 此行表示两次查询的间隔时间（单位：秒）
login_max_try = 10 # 此行表示最大尝试登陆次数


