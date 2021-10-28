import builtins

from flask import Flask,request

from demo.common import SerializerJsonResponse
from demo.global_var import dt_get_value



# Build paths inside the project like this: BASE_DIR / 'subdir'.
# sql injection
# Execute custom SQL statements;eg: sql=song
def mysql_post_e():
    db = dt_get_value("db")
    app = dt_get_value("app")
    sqlQuery = request.form['sql']

    rows = db.session.execute("select phone from user where name=:name_1", {"name_1": sqlQuery}, bind=db.get_engine(app, 'mysqlDb'))
    if rows:
        for line in rows:
            return SerializerJsonResponse({"phone": line[0]})
    else:
        return SerializerJsonResponse({"phone": ""})


# mysql批量执行
#  description=_("Batch execution of MySQL statements;eg: name=song,phone1=13322443212"),
# 未执行成功
def mysql_post_many():
    db = dt_get_value("db")
    app = dt_get_value("app")
    ser = request.form
    if ser:
        userName = ser['name']
        userPhone = ser['phone1']
    else:
        return SerializerJsonResponse(None, 202, "params error")
    exec_end = []
    sql = "insert into user(name, phone) values( % s, % s) "
    args = [(userName, 100), ("name1flask", userPhone)]
    # try:
    print(dir(db.session))
    exec_end = db.session.execute(sql, args, bind=db.get_engine(app, 'mysqlDb'))
    # except Exception as e:
    #     print("执行Mysql:")
    # print("----------")
    return SerializerJsonResponse({"result": exec_end})


# sqlite3 excute
#         description=_("Execute custom SQL statements;eg: sql=song"),
def sql_post_r(request):
    db = dt_get_value("db")
    app = dt_get_value("app")
    ser = request.form
    if ser.is_valid(True):
        sqlQuery = ser.validated_data['sql']
    else:
        return SerializerJsonResponse(None, 202, "params error")

    with db.get_session('sqlite3').cursor() as cursor:
        execEnd = cursor.execute("select phone from user where name= %s", [sqlQuery])
        endData = cursor.fetchone()
    print("----------")
    print(execEnd)
    print(endData)
    return SerializerJsonResponse({"phone": endData[0]})


# sqlite3 executemany
#                   description=_("Batch execution of sqlite3 executemany statements;eg: phone1=15523421232"),
def sql_post_executemany_sql(request):
    db = dt_get_value("db")
    app = dt_get_value("app")
    ser = request.form
    if ser.is_valid(True):
        phone1 = ser.validated_data['phone1']
    else:
        return SerializerJsonResponse(None, 202, "params error")

    sql = "insert into user (name, phone) values (?, ?);"
    data_list = [('张三1', phone1), ('李四1', 16655443311)]
    with db.get_session('sqlite3').cursor() as cursor:
        end = cursor.executemany(sql, data_list)
    return SerializerJsonResponse({})


# sqlite3 executescript
# description=_("Execute custom SQL statements of cursor.executescript,update phone1 by name;eg: phone1=15523421232,name=song"),
def sql_post_executescript(request):

    ser = request.form
    if ser.is_valid(True):
        phone1 = ser.validated_data['phone1']
        name = ser.validated_data['name']
    else:
        return SerializerJsonResponse(None, 202, "params error")
    sql_script = "update user set name='{}' where phone={}".format(name,phone1)
    print(sql_script)
    # with connections['sqlite3'].cursor() as cursor:
    #     end = cursor.executescript(sql_script)
    # print(end)
    return SerializerJsonResponse({})





# Execute custom SQL of pysql statements ;eg: sql=song
def pysql_post_excute(request):

    ser = request.form
    if ser.is_valid(True):
        sqlQuery = ser.validated_data['sql']
    else:
        return SerializerJsonResponse(None, 202, "params error")
    with db.get_session('pySqlDb').cursor()  as cursor:
        execEnd = cursor.execute("select phone from muser where name=%s",[sqlQuery])
        endData = cursor.fetchone()
    print("----------")
    print(execEnd)
    print(endData)
    return SerializerJsonResponse({"phone": endData[0]})


# pysql 批量执行
# description=_("Execute custom SQL of pysql statements ;eg: name=song,phone1=16654321232,id=100"),
def pysql_post_many(request):
    ser = request.form
    if ser.is_valid(True):
        userName = ser.validated_data['name']
        userPhone = ser.validated_data['phone1']
        userId = ser.validated_data['id']
    else:
        return SerializerJsonResponse(None, 202, "params error")
    exec_end = []

    with db.get_session('pySqlDb').cursor()  as cursor:

        sql = "insert into muser(id, name, phone) values( %s,  %s, %s) "
        args = [(userId, userName, "100"), (str(int(userId)+1), "name1", userPhone)]
        try:
            exec_end = cursor.executemany(sql, args)
        except Exception as e:
            print(e)
            exec_end = 0

    print("----------")
    return SerializerJsonResponse(exec_end)