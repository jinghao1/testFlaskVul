from app import db

def mysqlExcute(app,sqlQuery):
    rows = db.session.execute("select phone from user where name= %s", [sqlQuery], bind=db.get_engine(app, 'mysqlDb'))
    return rows