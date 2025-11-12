from flask import Flask, url_for, request, redirect, abort, render_template
import os
import datetime
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB-TYPE', 'postgres')

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)

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
