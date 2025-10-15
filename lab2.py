from flask import Blueprint, url_for, request, redirect, abort, render_template
lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/a')
def a1():
    return 'без слэша'

@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'

flowers = [
    {"name": "роза", "price": 300},
    {"name": "тюльпан", "price": 310},
    {"name": "незабудка", "price": 320},
    {"name": "ромашка", "price": 330},
    {"name": "георгин", "price": 300},
    {"name": "гладиолус", "price": 310},
]


@lab2.route("/lab2/flowers")
def all_flowers():
    return render_template("lab2/flowers.html", flowers=flowers)


@lab2.route("/lab2/del_flower/<int:flower_id>")
def del_flower(flower_id):
    if 1 <= flower_id <= len(flowers):
        flowers.pop(flower_id - 1)
        return redirect(url_for("all_flowers"))
    else:
        abort(404)


@lab2.route("/lab2/clear_flowers")
def clear_flowers():
    flowers.clear()
    return redirect(url_for("all_flowers"))


@lab2.route("/lab2/add_flower", methods=["POST"])
def add_flower():
    name = request.form.get("name")
    price = request.form.get("price")
    if name and price.isdigit():
        flowers.lab2end({"name": name, "price": int(price)})
    return redirect(url_for("all_flowers"))


@lab2.route('/lab2/example')
def example():
    name, lab_num, group, course = 'Иван Стародубцев', 2, 'ФБИ-31', 3
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('lab2/example.html',
                           name=name, lab_num=lab_num, group=group,
                           course=course, fruits=fruits)


@lab2.route('/lab2/')
def lab():
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase=phrase)


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')


@lab2.route('/lab2/calc/<int:a>')
def calc_one(a):
    return redirect(f'/lab2/calc/{a}/1')


@lab2.route('/lab2/calc/<int:a>/<int:b>')
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


@lab2.route('/lab2/books')
def show_books():
    return render_template('lab2/books.html', books=books)


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


@lab2.route('/lab2/cars')
def show_cars():
    return render_template('lab2/cars.html', cars=cars)
