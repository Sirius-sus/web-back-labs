from flask import Flask, url_for, request, redirect, abort
import datetime
app = Flask(__name__)

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
        </ul>
        <footer>Стародубцев Иван Алексеевич, ФБИ-31, 3 курс, 2025</footer>
    </body>
</html>
'''

@app.route("/lab1")
def lab1():
    return '''
<!doctype html>
<html>
    <head><title>Лабораторная 1</title></head>
    <body>
        <p>
            Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
        </p>
        <a href="/">Вернуться на главную</a>
        <h2>Список роутов</h2>
        <ul>
            <li><a href="/lab1/web">/lab1/web</a></li>
            <li><a href="/lab1/author">/lab1/author</a></li>
            <li><a href="/lab1/image">/lab1/image</a></li>
            <li><a href="/lab1/counter">/lab1/counter</a></li>
            <li><a href="/lab1/clear_counter">/lab1/clear_counter</a></li>
            <li><a href="/lab1/info">/lab1/info</a></li>
            <li><a href="/lab1/created">/lab1/created</a></li>
            <li><a href="/400">/400</a></li>
            <li><a href="/401">/401</a></li>
            <li><a href="/402">/402</a></li>
            <li><a href="/403">/403</a></li>
            <li><a href="/405">/405</a></li>
            <li><a href="/418">/418</a></li>
            <li><a href="/500">/500</a></li>
        </ul>
    </body>
</html>
'''


@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
            <body>
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a>
            </body>
        </html>""", 200, {
            'X-server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }

@app.route("/lab1/author")
def author():
    name = "Стародубцев Иван Алексеевич"
    group = "ФБИ-31"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
               <p>Студент: """ + name + """</p>
               <p>Группа: """ + group + """</p>
               <p>Факультет: """ + faculty + """</p>
               <a href="/lab1/web">web</a>
            </body>
        </html>"""

@app.route("/lab1/image")
def image():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="''' + path + '''">
    </body>
</html>
''', 200, {
    'Content-Language': 'ru',
    'X-Server': 'Flask-Sample',
    'X-Custom-Header': 'Lab1'
}

count = 0

@app.route("/lab1/counter")
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP-адрес: ''' + client_ip + '''<br>
        <a href="/lab1/clear_counter">Очистить счётчик</a>
    </body>
</html>
'''

@app.route("/lab1/clear_counter")
def clear_counter():
    global count
    count = 0
    return redirect("/lab1/counter")

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>Что-то создано...</i></div>
    </body>
</html>
''', 201

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

@app.route("/400")
def err400():
    return "Некорректный запрос", 400

@app.route("/401")
def err401():
    return "Не авторизован", 401

@app.route("/402")
def err402():
    return "Необходима оплата", 402

@app.route("/403")
def err403():
    return "Запрещено", 403

@app.route("/405")
def err405():
    return "Метод не поддерживается", 405

@app.route("/418")
def err418():
    return "Я - чайник", 418

@app.route("/500")
def error500():
    return 1/0

@app.errorhandler(500)
def internal_error(err):
    return "Внутренняя ошибка сервера", 500

@app.route('/lab2/a')
def a1():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ('роза', 'тюльпан', 'незабудка', 'ромашка')

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return 'id=' + flower_list[flower_id]