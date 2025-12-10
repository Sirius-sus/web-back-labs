from flask import Flask, url_for, request, redirect, abort, render_template
import os
from os import path
import datetime
from flask_sqlalchemy import SQLAlchemy
from db import db
from db.models import users
from flask_login import LoginManager

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9

app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_users(login_id):
    return users.query.get(int(login_id))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')


if app.config['DB_TYPE'] == 'postgres':
    db_name = 'ivan_starodubtsev_orm'
    db_user = 'ivan_starodubtsev_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "ivan_starodubtsev_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)

@app.route("/")
@app.route("/index")
def index():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        <ul>
            <li><a href="/lab1">Первая лабораторная</a></li>
            <li><a href="/lab2">Вторая лабораторная</a></li>
            <li><a href="/lab3">Третья лабораторная</a></li>
            <li><a href="/lab4">Четвёртая лабораторная</a></li>
            <li><a href="/lab5">Пятая лабораторная</a></li>
            <li><a href="/lab6">Шестая лабораторная</a></li>
            <li><a href="/lab7">Седьмая лабораторная</a></li>
            <li><a href="/lab8">Восьмая лабораторная</a></li>
            <li><a href="/lab9">Девятая лабораторная</a></li>
        </ul>
        <footer>Стародубцев Иван Алексеевич, ФБИ-31, 3 курс, 2025</footer>
    </body>
</html>
'''

log_404 = []

@app.errorhandler(404)
def not_found(err):
    time = datetime.datetime.now()
    client_ip = request.remote_addr
    requested_url = request.url

    log_404.append(f"[{time}] пользователь {client_ip} зашёл на адрес: {requested_url}")

    path = url_for("static", filename="okak.jpg")
    log_html = "<br>".join(log_404)
    return '''
<!doctype html>
<html>
    <style>
        body {
            background-color: #111111;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
        }
        img {
            width: 400px;
        }
    </style>
    <body>
        <h1>Окак! Страница не найдена</h1>
        <h2>Ошибка 404</h2>
        <img src="''' + path + '''">
        <p>Ваш IP-адрес: ''' + client_ip + '''</p>
        <p>Дата и время доступа: ''' + str(time) + '''</p>
        <p><a href="/">Вернуться на главную</a></p>
        <hr>
        <h3>Журнал посещений 404:</h3>
        ''' + log_html + '''
    </body>
</html>
'''


@app.errorhandler(500)
def internal_error(err):
    return "Внутренняя ошибка сервера", 500
