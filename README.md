# flask-blog-owner
通过Flask框架搭建的个人博客网站。

#### Start
##### 1.安装依赖文件
```shell script
cd flask-owner-blog
pip install -r requirement.txt -i https://pypi.douban.com/simple
```
##### 2.初始化数据库
```shell script
cd migrate
python init_db.py
```
##### 3.运行
1. Windows
```shell script
cd flask-owner-blog
set FLASK_APP=app
set FLASK_ENV=development # 可选
# 下面的命令二选一即可
python -m flask run # 不指定主机及端口号
python -m flask run --host=0.0.0.0 --port=8000 # 指定主机及端口号
```
2. Linux
```shell script
cd flask-owner-blog
export FLASK_APP=app
export FLASK_ENV=development 
# 下面的命令二选一即可
flask run # 不指定主机及端口号
flask run --host=0.0.0.0 --port=8000 # 指定主机及端口号
```
如果采用不指定主机以及端口号的运行方式，访问`127.0.0.1:5000`，即可以看到博客主页。
如果采用指定主机以及端口号的运行方式，访问`youridp:yourport`，既可以看到博客主页。

> 示例图
![alt 博客主页](https://github.com/weijiang1994/flask-blog-owner/blob/master/screenshot/homePage.jpg
)
