from flask import Flask, url_for, request, redirect, abort, render_template
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
            <li><a href="/lab2">Вторая лабораторная</a></li>
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

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers')
def flowers_all():
    total = len(flower_list)
    items = "".join(f"<li>{i+1}. {name}</li>" for i, name in enumerate(flower_list))
    return f'''
<!doctype html>
<html>
    <head><meta charset="utf-8"><title>Список цветов</title></head>
    <body>
        <h1>Список цветов</h1>
        <p>Всего цветов: {total}</p>
        <ul>
            {items}
        </ul>
        <p><a href="/lab2/clear_flowers">Очистить список цветов</a></p>
        <p><a href="/lab2/">Вернуться в лаб.2</a></p>
    </body>
</html>
'''

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    name = flower_list[flower_id]
    list_url = url_for('flowers_all')
    return f'''
<!doctype html>
<html>
    <head><meta charset="utf-8"><title>Цветок {name}</title></head>
    <body>
        <h1>Информация о цветке</h1>
        <p>id = {flower_id}</p>
        <p>название: <b>{name}</b></p>
        <p><a href="{list_url}">Показать все цветы</a></p>
        <p><a href="/lab2/">Вернуться в лаб.2</a></p>
    </body>
</html>
'''
    
@app.route('/lab2/add_flower/')
def add_flower_no_name():
    return "вы не задали имя цветка", 400
    
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
        <h1>Добавлен новый цветок</h1>
        <p>Название нового цветка: {name} </p>
        <p>Всего цветов: {len(flower_list)}</p>
        <p>Полный список: {flower_list}</p>
    </body>
</html>
'''

@app.route('/lab2/clear_flowers')
def clear_flowers():
    global flower_list
    flower_list = []
    return f'''
<!doctype html>
<html>
    <head><meta charset="utf-8"><title>Список очищен</title></head>
    <body>
        <h1>Список цветов очищен</h1>
        <p>Теперь цветов: {len(flower_list)}</p>
        <p><a href="{url_for('flowers_all')}">Показать все цветы</a></p>
        <p><a href="/lab2/">Вернуться в лаб.2</a></p>
    </body>
</html>
'''

@app.route('/lab2/example')
def example():
    name, lab_num, group, course = 'Иван Стародубцев', 2, 'ФБИ-31', 3
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html',
                           name=name, lab_num=lab_num, group=group,
                           course=course, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

@app.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_one(a):
    return redirect(f'/lab2/calc/{a}/1')

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    add = a + b
    sub = a - b
    mul = a * b
    if b == 0:
        div = "деление на ноль"
    else:
        div = f"{a / b:.2f}".replace('.', ',')
    powr = a ** b
    return f'''
<!doctype html>
<html>
    <head><meta charset="utf-8"><title>Калькулятор: {a} и {b}</title></head>
    <body>
        <h1>Расчёт с параметрами:</h1>
        <p>{a} + {b} = {add}</p>
        <p>{a} - {b} = {sub}</p>
        <p>{a} × {b} = {mul}</p>
        <p>{a} / {b} = {div}</p>
        <p>{a}<sup>{b}</sup> = {powr}</p>
        <p><a href="/lab2/">Вернуться в лаб.2</a></p>
    </body>
</html>
'''

books = [
    {"title": "Преступление и наказание", "author": "Ф. Достоевский", "genre": "роман", "pages": 671},
    {"title": "Мастер и Маргарита", "author": "М. Булгаков", "genre": "роман", "pages": 480},
    {"title": "Война и мир", "author": "Л. Толстой", "genre": "эпопея", "pages": 1225},
    {"title": "Гарри Поттер и философский камень", "author": "Дж. Роулинг", "genre": "фэнтези", "pages": 352},
    {"title": "1984", "author": "Дж. Оруэлл", "genre": "антиутопия", "pages": 328},
    {"title": "Маленький принц", "author": "А. де Сент-Экзюпери", "genre": "сказка", "pages": 96},
    {"title": "Анна Каренина", "author": "Л. Толстой", "genre": "роман", "pages": 864},
    {"title": "Шерлок Холмс", "author": "А. Конан Дойл", "genre": "детектив", "pages": 560},
    {"title": "Обломов", "author": "И. Гончаров", "genre": "роман", "pages": 608},
    {"title": "Три мушкетёра", "author": "А. Дюма", "genre": "роман", "pages": 704}
]

@app.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)

cars = [
    {"name": "BMW M3", "desc": "Спортивный седан", "img": "cars/bmw_m3.jpg"},
    {"name": "Audi A6", "desc": "Бизнес-седан", "img": "cars/audi_a6.jpg"},
    {"name": "Mercedes-Benz E-Class", "desc": "Комфорт и престиж", "img": "cars/mercedes_e.jpg"},
    {"name": "Toyota Camry", "desc": "Надёжный седан", "img": "cars/toyota_camry.jpg"},
    {"name": "Honda Civic", "desc": "Компактный и экономичный", "img": "cars/honda_civic.jpg"},
    {"name": "Ford Mustang", "desc": "Знаковое американское купе", "img": "cars/ford_mustang.jpg"},
    {"name": "Chevrolet Camaro", "desc": "Купе с характером", "img": "cars/chevrolet_camaro.jpg"},
    {"name": "Tesla Model S", "desc": "Электроседан с автопилотом", "img": "cars/tesla_model_s.jpg"},
    {"name": "Porsche 911", "desc": "Классическое спортивное купе", "img": "cars/porsche_911.jpg"},
    {"name": "Lamborghini Aventador", "desc": "Суперкар для скорости", "img": "cars/lamborghini_aventador.jpg"},
    {"name": "Ferrari 488", "desc": "Итальянский суперкар", "img": "cars/ferrari_488.jpg"},
    {"name": "Nissan GT-R", "desc": "Японская легенда", "img": "cars/nissan_gtr.jpg"},
    {"name": "Mazda MX-5", "desc": "Компактный родстер", "img": "cars/mazda_mx5.jpg"},
    {"name": "Volkswagen Golf", "desc": "Немецкий хэтчбек", "img": "cars/vw_golf.jpg"},
    {"name": "Kia Sportage", "desc": "Популярный кроссовер", "img": "cars/kia_sportage.jpg"},
    {"name": "Hyundai Tucson", "desc": "Универсальный кроссовер", "img": "cars/hyundai_tucson.jpg"},
    {"name": "Jeep Wrangler", "desc": "Внедорожник для приключений", "img": "cars/jeep_wrangler.jpg"},
    {"name": "Range Rover", "desc": "Премиальный внедорожник", "img": "cars/range_rover.jpg"},
    {"name": "Subaru Impreza WRX", "desc": "Ралли-легенда", "img": "cars/subaru_wrx.jpg"},
    {"name": "Mitsubishi Lancer Evo", "desc": "Ралли-классика", "img": "cars/mitsubishi_evo.jpg"}
]

@app.route('/lab2/cars')
def show_cars():
    return render_template('cars.html', cars=cars)
