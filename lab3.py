from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    if name is None:
        name = "Аноним"
    if age is None:
        age = "неизвестно"
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_weight = request.args.get('font_weight')
    
    if any([color, bg_color, font_size, font_weight]):
        resp = make_response(redirect('/lab3/settings'))
        
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_weight:
            resp.set_cookie('font_weight', font_weight)
            
        return resp
    
    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    font_weight = request.cookies.get('font_weight')
    resp = make_response(render_template('lab3/settings.html', color=color, bg_color=bg_color, font_size=font_size, font_weight=font_weight))
    return resp

@lab3.route('/lab3/ticket')
def ticket():
    errors = {}
    fio = request.args.get('fio')
    age = request.args.get('age')
    berth = request.args.get('berth')
    linen = request.args.get('linen')
    luggage = request.args.get('luggage')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance')

    # Проверки на пустые поля
    if fio == '' or fio is None:
        errors['fio'] = 'Заполните поле!'
    if age == '' or age is None:
        errors['age'] = 'Заполните поле!'
    elif not age.isdigit() or not (1 <= int(age) <= 120):
        errors['age'] = 'Возраст должен быть от 1 до 120!'
    if berth == '' or berth is None:
        errors['berth'] = 'Выберите полку!'
    if linen == '' or linen is None:
        errors['linen'] = 'Укажите наличие белья!'
    if luggage == '' or luggage is None:
        errors['luggage'] = 'Укажите наличие багажа!'
    if departure == '' or departure is None:
        errors['departure'] = 'Заполните поле!'
    if destination == '' or destination is None:
        errors['destination'] = 'Заполните поле!'
    if date == '' or date is None:
        errors['date'] = 'Укажите дату!'
    if insurance == '' or insurance is None:
        errors['insurance'] = 'Укажите, нужна ли страховка!'

    # Если есть ошибки — просто показать форму с подсказками
    if errors:
        return render_template('lab3/ticket.html', fio=fio, age=age, berth=berth,
                               linen=linen, luggage=luggage, departure=departure,
                               destination=destination, date=date, insurance=insurance,
                               errors=errors)

    # Расчёт цены
    if int(age) < 18:
        price = 700
    else:
        price = 1000

    if berth in ['нижняя', 'нижняя боковая']:
        price += 100
    if linen == 'yes':
        price += 75
    if luggage == 'yes':
        price += 250
    if insurance == 'yes':
        price += 150

    return render_template('lab3/ticket.html', fio=fio, age=age, berth=berth,
                           linen=linen, luggage=luggage, departure=departure,
                           destination=destination, date=date, insurance=insurance,
                           price=price, errors={})

@lab3.route('/lab3/del_settings_cookies')
def del_settings_cookies():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('font_weight')
    return resp

@lab3.route('/lab3/books')
def books():
    # Список книг (можно расширить)
    books = [
        {"title": "Преступление и наказание", "price": 850, "author": "Ф. Достоевский", "genre": "роман"},
        {"title": "Мастер и Маргарита", "price": 950, "author": "М. Булгаков", "genre": "мистика"},
        {"title": "Война и мир", "price": 1200, "author": "Л. Толстой", "genre": "исторический"},
        {"title": "Анна Каренина", "price": 1000, "author": "Л. Толстой", "genre": "роман"},
        {"title": "Отцы и дети", "price": 700, "author": "И. Тургенев", "genre": "философский"},
        {"title": "Евгений Онегин", "price": 600, "author": "А. Пушкин", "genre": "поэма"},
        {"title": "Дубровский", "price": 550, "author": "А. Пушкин", "genre": "приключения"},
        {"title": "Маленький принц", "price": 500, "author": "А. де Сент-Экзюпери", "genre": "сказка"},
        {"title": "1984", "price": 800, "author": "Дж. Оруэлл", "genre": "антиутопия"},
        {"title": "Мы", "price": 650, "author": "Е. Замятин", "genre": "антиутопия"},
        {"title": "Собачье сердце", "price": 750, "author": "М. Булгаков", "genre": "сатиры"},
        {"title": "Идиот", "price": 900, "author": "Ф. Достоевский", "genre": "роман"},
        {"title": "Белая гвардия", "price": 870, "author": "М. Булгаков", "genre": "исторический"},
        {"title": "Герой нашего времени", "price": 780, "author": "М. Лермонтов", "genre": "роман"},
        {"title": "Хаджи-Мурат", "price": 670, "author": "Л. Толстой", "genre": "повесть"},
        {"title": "Обломов", "price": 950, "author": "И. Гончаров", "genre": "роман"},
        {"title": "Доктор Живаго", "price": 1100, "author": "Б. Пастернак", "genre": "драма"},
        {"title": "Тихий Дон", "price": 1300, "author": "М. Шолохов", "genre": "эпопея"},
        {"title": "Пиковая дама", "price": 400, "author": "А. Пушкин", "genre": "новелла"},
        {"title": "Шинель", "price": 480, "author": "Н. Гоголь", "genre": "рассказ"},
    ]

    global_min = min(book["price"] for book in books)
    global_max = max(book["price"] for book in books)

    # Получаем данные из запроса или куки
    action = request.args.get('action')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    if not min_price:
        min_price = request.cookies.get('min_price')
    if not max_price:
        max_price = request.cookies.get('max_price')

    # Обработка кнопки "Сброс"
    if action == 'reset':
        resp = make_response(render_template('lab3/books.html', books=books,
                                             global_min=global_min, global_max=global_max,
                                             min_price='', max_price=''))
        resp.delete_cookie('min_price')
        resp.delete_cookie('max_price')
        return resp

    if min_price and max_price:
        try:
            min_val = float(min_price)
            max_val = float(max_price)
            if min_val > max_val:
                min_val, max_val = max_val, min_val
        except ValueError:
            min_val, max_val = None, None
    else:
        min_val = float(min_price) if min_price else None
        max_val = float(max_price) if max_price else None

    filtered_books = []
    for book in books:
        price = book["price"]
        if (min_val is None or price >= min_val) and (max_val is None or price <= max_val):
            filtered_books.append(book)

    resp = make_response(render_template('lab3/books.html',
                                         books=filtered_books,
                                         global_min=global_min,
                                         global_max=global_max,
                                         min_price=min_price,
                                         max_price=max_price))
    if action == 'search':
        if min_price:
            resp.set_cookie('min_price', str(min_price))
        if max_price:
            resp.set_cookie('max_price', str(max_price))

    return resp