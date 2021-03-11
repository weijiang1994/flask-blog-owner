# flask-blog-owner
通过Flask框架搭建的个人博客网站。
# :warning: 此版本不再进行更新! 
# :star: [移步新版Blogin](https://github.com/weijiang1994/Blogin)
#### Start
[English Guid](https://github.com/weijiang1994/flask-blog-owner/blob/master/README-EN.md)
##### 1.安装依赖文件
```shell script
cd flask-blog-owner
pip install -r requirement.txt -i https://pypi.douban.com/simple
```
##### 2.初始化数据库
> 在进行这个步骤之前你需要提前先安装一个使用的数据库。
```shell script
cd flask-blog-owner/init/migrate
python init_db.py
```
运行过程中需要你输入你数据库的相关信息，根据提示正确输入即可。
##### 3. 初始化配置文件
为了数据库安全，仓库没有上传配置文件的相关内容，因此需要自己新建配置文件
```shell script
cd flask-blog-owner/app/
mkdir config
vim config.ini
```
在`config.ini`文件中输入如下内容，具体信息根据自己数据库配置而定。
```editorconfig
[DATABASE]
host=your_db_host
port=your_db_port
user=your_db_user
password=your_db_password
database=blogin
```
##### 4.运行
1. Windows
```shell script
cd flask-blog-owner
set FLASK_APP=app
set FLASK_ENV=development # 可选
# 下面的命令二选一即可
python -m flask run # 不指定主机及端口号
python -m flask run --host=0.0.0.0 --port=8000 # 指定主机及端口号
```
2. Linux
```shell script
cd flask-blog-owner
export FLASK_APP=app
export FLASK_ENV=development 
# 下面的命令二选一即可
flask run # 不指定主机及端口号
flask run --host=0.0.0.0 --port=8000 # 指定主机及端口号
```
如果采用不指定主机以及端口号的运行方式，访问`127.0.0.1:5000`，即可以看到博客主页。
如果采用指定主机以及端口号的运行方式，访问`yourip:yourport`，既可以看到博客主页。

> 示例图

![alt 博客主页](https://github.com/weijiang1994/flask-blog-owner/blob/master/screenshot/homePage.jpg
)

##### 5.演示地址
传送门:http://2dogz.cn
