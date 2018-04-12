# ustc-yjs-course-hacker

USTC 研究生平台自动刷课脚本
—————基于zzh1996的[项目](https://github.com/zzh1996/ustc-grade-automatic-notification)


### 简介

这是一个针对中国科学技术大学研究生教务系统（[yjs.ustc.edu.cn](http://yjs.ustc.edu.cn/)）的自动选课脚本，可以自动登录教务系统（基于 zhsj 的 [项目](https://github.com/zhsj/ustcmis)），并定时查询课程是否有空余名额，若有空余名额则以邮件形式通知用户，并尝试自动选课。

本程序未经严格测试，不保证提供服务的稳定性。

### 使用方法（以 Win10 为例）

1、下载代码

```shell
git clone https://github.com/ustcjerry/ustc-yjs-course-hacker.git
```

2、修改配置文件

```shell
cd ustc-yjs-course-hacker
cp config_example.py config.py
vim config.py
vim autorun.bat
```

配置文件中各个参数的含义请参考每行后面的注释

请根据注释修改 `main.py` 中的课程信息

3、运行

```
python main.py
```

4、自动运行bat脚本

```
./autorun.bat
```

查询到有空余名额后会发送一封通知邮件，并尝试自动选课。

### 基于

```
python3
OpenCV 
matplotlib
requests
numpy
selenium
bs4
smtplib
```

### TODO

- [x] 成功识别验证码
- [x] 使用统一身份认证平台登录
- [x] 使用验证码登录yjs平台



