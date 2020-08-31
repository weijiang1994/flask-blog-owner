# flask-blog-owner
A personal blog site built through the Flask framework.

#### Start
[中文指引](https://github.com/weijiang1994/flask-blog-owner/blob/master/README.md)
##### 1.Install requirements
```shell script
cd flask-blog-owner
pip install -r requirement.txt
```
##### 2.Initial database
> You need install a database software like mysql or mariadb before this step!
```shell script
cd flask-blog-owner/init/migrate
python init_db.py
```
You need to enter the relevant information of your database during the running process, just enter it correctly according to the prompts.
##### 3. Initial config file
For database security, the repository does not upload the configuration file, so you need to create a new configuration file by yourself.
```shell script
cd flask-blog-owner/app/
mkdir config
vim config.ini
```
Enter the following content in the config.ini file, the specific information depends on your own database configuration.
```editorconfig
[DATABASE]
host=your_db_host
port=your_db_port
user=your_db_user
password=your_db_password
database=blogin
```
##### 4.Run
1. Windows
```shell script
cd flask-blog-owner
set FLASK_APP=app
set FLASK_ENV=development # option
# Choose one of the following commands to run.
python -m flask run # not declare host and port
python -m flask run --host=0.0.0.0 --port=8000 # declare host and port
```
2. Linux
```shell script
cd flask-blog-owner
export FLASK_APP=app
export FLASK_ENV=development # option
# Choose one of the following commands to run.
flask run # not declare host and port
flask run --host=0.0.0.0 --port=8000 # declare host and port
```
If the operation mode does not specify the host and port number，visit `127.0.0.1:5000`，and you can see the blog homepage.
If you use the specified host and port number operation mode, visit `yourip:yourport`, you can see the blog homepage.

> Sample Image

![alt 博客主页](https://github.com/weijiang1994/flask-blog-owner/blob/master/screenshot/homePage.jpg
)

##### 5.Blog Online Address
addr:http://2dogz.cn