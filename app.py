from flask import Flask
import os
from routes import setup_routes
from flask_sqlalchemy import SQLAlchemy
# from demo.sql_injection import sql_api
from demo.global_var import dt_set_value
app = Flask(__name__)

curDir = os.path.dirname(__file__)

sqlitePath = str(os.path.join(curDir, "db.sqlite3"))
app.config['SQLALCHEMY_BINDS'] = {
    "sqlite3": "sqlite:///"+sqlitePath,
    "mysqlDb": "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format("root", "1823song", "127.0.0.1", "3306", "dc_strategy"),
    "pySqlDb": "postgres://{}:{}@{}:{}/{}".format("postgres", "1823songG", "127.0.0.1", "5432", "mysite")
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# from dongtai_agent_python.middlewares.flask_middleware import AgentMiddleware
# app.wsgi_app = AgentMiddleware(app.wsgi_app, app)

db = SQLAlchemy(app)
dt_set_value("app",app)
dt_set_value("db",db)
# @app.route('/login', methods=[ 'POST'])
# def mysql_post_e_fun():
#     result = sql_api.mysql_post_e(app, db)
#     return result
setup_routes(app)

if __name__ == '__main__':
    app.run()
