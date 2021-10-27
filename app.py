from flask import Flask
from dongtai_agent_python.middlewares.flask_middleware import AgentMiddleware

app = Flask(__name__)
app.wsgi_app = AgentMiddleware(app.wsgi_app, app)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
