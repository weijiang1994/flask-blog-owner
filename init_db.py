import pymysql

# host = '192.168.43.14'
# port = 3306
# username = 'root'
# pwd = '19940124'

print('initial the database, please input require information of the database that you want to connect.')
host = input('please input database host:')
port = input('please input database port:')
username = input('please input database login username:')
pwd = input('please input database ;login password:')


print('test connect...')
try:
    conn = pymysql.connect(host=host, port=int(port), user=username, password=pwd)
    cur = conn.cursor()
    print('database connect successful.')
except Exception as e:
    print('database connect fail, please check the error and retry.')
    print(e.args)
try:
    conti = input('initial database will clear the destination database data, do you want to continue?(y/n)')
    if conti == 'y':
        print('-----------------------------------------------------------')
        print('create database...')
        # cur.execute("drop database if exists blogin")
        cur.execute('create database if not exists blogin')
        print('database created done.')
        conn.select_db('blogin')
        print('-----------------------------------------------------------')
        print('create admin table...')
        cur.execute("drop table if exists admin")
        cur.execute("create table if not exists admin("
                    "id VARCHAR(40) PRIMARY KEY,"
                    "user_name VARCHAR(255) NOT NULL,"
                    "password VARCHAR(255) NOT NULL)")
        print('create admin table done...')
        print('-----------------------------------------------------------')
        print('create timeline table...')
        cur.execute("drop table if exists timeline")
        cur.execute("create table if not exists timeline("
                    "id VARCHAR(40) PRIMARY KEY NOT NULL,"
                    "title VARCHAR(255) NOT NULL,"
                    "content VARCHAR(1024) NOT NULL,"
                    "time DateTime)")
        print('create timeline table done...')
        print('-----------------------------------------------------------')
        print('create blog_type table...')
        cur.execute("drop table if exists blog_type")
        cur.execute("create table if not exists blog_type("
                    "id VARCHAR(40) PRIMARY KEY NOT NULL,"
                    "type_name VARCHAR(40) NOT NULL,"
                    "create_time DateTime,"
                    "blog_count INTEGER(11) NOT NULL,"
                    "description VARCHAR(1024) NOT NULL)")
        print('create blog_type table done...')
        print('-----------------------------------------------------------')
        print('create table article...')
        cur.execute("drop table if exists article")
        cur.execute("create table if not exists article("
                    "id VARCHAR(40) PRIMARY KEY NOT NULL,"
                    "title VARCHAR(255) NOT NULL,"
                    "type INTEGER(11) NOT NULL,"
                    "img VARCHAR(255) NOT NULL,"
                    "brief_content VARCHAR(255) NOT NULL,"
                    "content Text NOT NULL,"
                    "private INTEGER(11) NOT NULL,"
                    "create_time DateTime,"
                    "update_time DateTime,"
                    "read_times INTEGER(11) NOT NULL,"
                    "delete_flag INTEGER(11) NOT NULL)")
        print('create article table done...')
        print('-----------------------------------------------------------')
        print('create comment table...')
        cur.execute("drop table if exists comment")
        cur.execute("create table if not exists comment("
                    "id VARCHAR(40) PRIMARY KEY NOT NULL,"
                    "article_id VARCHAR(40) NOT NULL,"
                    "parent_id VARCHAR(40) NOT NULL,"
                    "comment_time DateTime,"
                    "comment_content VARCHAR(255) NOT NULL,"
                    "is_read INTEGER(11) NOT NULL,"
                    "delete_flag INTEGER(11) NOT NULL"
                    ")")
        print('create comment table done...')
        print('-----------------------------------------------------------')
        conn.commit()
        cur.close()
        conn.close()
        print('operator successful.')
        print('exit')
    else:
        print('Not execute any operator.')
        print('exit.')
except Exception as e:
    raise
