from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    if x2 == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя!')
    
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    x1 = int(x1) if x1 != '' else 0
    x2 = int(x2) if x2 != '' else 0
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    x1 = int(x1) if x1 != '' else 1
    x2 = int(x2) if x2 != '' else 1
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)

# Возведение в степень
@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def pow():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='Оба числа не могут быть равны нулю!')
    
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)

tree_count = 0

@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < 10:
        tree_count += 1
    
    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': '123', 'name': 'Алексей Иванов', 'gender': 'м'},
    {'login': 'bob', 'password': '555', 'name': 'Борис Смирнов', 'gender': 'м'},
    {'login': 'ivan', 'password': '777', 'name': 'Иван Стародубцев', 'gender': 'м'},
    {'login': 'sirius', 'password': 'sus', 'name': 'Sirius Sus', 'gender': 'м'},
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            name = session.get('name')
        else:
            authorized = False
            login = ''
            name = ''
        return render_template("lab4/login.html", authorized=authorized, login=login, name=name)

    login = request.form.get('login')
    password = request.form.get('password')

    if login == '':
        return render_template('lab4/login.html', error='Не введён логин', authorized=False, login=login)
    if password == '':
        return render_template('lab4/login.html', error='Не введён пароль', authorized=False, login=login)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            session['name'] = user['name']
            return redirect('/lab4/login')

    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=login)

@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        return render_template('lab4/fridge.html')

    temp = request.form.get('temp')

    if temp == '':
        return render_template('lab4/fridge.html', error='Ошибка: не задана температура')

    temp = int(temp)
    
    if temp < -12:
        message = 'Не удалось установить температуру — слишком низкое значение'
        return render_template('lab4/fridge.html', error=message)
    elif temp > -1:
        message = 'Не удалось установить температуру — слишком высокое значение'
        return render_template('lab4/fridge.html', error=message)
    else:
        message = f'Установлена температура: {temp}°C'
        if -12 <= temp <= -9:
            snowflakes = 3
        elif -8 <= temp <= -5:
            snowflakes = 2
        elif -4 <= temp <= -1:
            snowflakes = 1
        else:
            snowflakes = 0
        return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes)

@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain():
    prices = {
        'ячмень': 12000,
        'овёс': 8500,
        'пшеница': 9000,
        'рожь': 15000
    }

    if request.method == 'GET':
        return render_template('lab4/grain.html', prices=prices)

    grain_type = request.form.get('grain')
    weight = request.form.get('weight')

    if weight == '':
        return render_template('lab4/grain.html', error='Ошибка: не указан вес', prices=prices)

    weight = float(weight)
    
    if weight <= 0:
        return render_template('lab4/grain.html', error='Ошибка: вес должен быть больше 0', prices=prices)

    if weight > 100:
        return render_template('lab4/grain.html', error='Такого объёма сейчас нет в наличии', prices=prices)

    price_per_ton = prices.get(grain_type)
    total = price_per_ton * weight
    discount_text = ''

    if weight > 10:
        discount = total * 0.10
        total -= discount
        discount_text = f'Применена скидка 10% за большой объём (-{int(discount)} руб).'
    
    message = f'Заказ успешно сформирован. Вы заказали {grain_type}. Вес: {weight} т. Сумма к оплате: {int(total)} руб.'
    
    return render_template('lab4/grain.html', message=message, discount=discount_text, prices=prices)

@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab4/register.html')

    login = request.form.get('login')
    name = request.form.get('name')
    password = request.form.get('password')
    confirm = request.form.get('confirm')
    gender = request.form.get('gender')

    if not login or not name or not password or not confirm:
        return render_template('lab4/register.html', error='Все поля должны быть заполнены!', login=login, name=name)

    for user in users:
        if user['login'] == login:
            return render_template('lab4/register.html', error='Такой логин уже существует!', login=login, name=name)

    if password != confirm:
        return render_template('lab4/register.html', error='Пароли не совпадают!', login=login, name=name)

    users.append({'login': login, 'password': password, 'name': name, 'gender': gender})
    session['login'] = login
    session['name'] = name
    return redirect('/lab4/login')

@lab4.route('/lab4/users')
def users_list():
    if 'login' not in session:
        return redirect('/lab4/login')
    return render_template('lab4/users.html', users=users, current_user=session['login'])

@lab4.route('/lab4/delete', methods=['POST'])
def delete_self():
    if 'login' not in session:
        return redirect('/lab4/login')
    global users
    users = [u for u in users if u['login'] != session['login']]
    session.pop('login', None)
    session.pop('name', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/edit', methods=['GET', 'POST'])
def edit():
    if 'login' not in session:
        return redirect('/lab4/login')

    login = session['login']
    user = next((u for u in users if u['login'] == login), None)

    if request.method == 'GET':
        return render_template('lab4/edit.html', user=user)

    new_login = request.form.get('login')
    new_name = request.form.get('name')
    new_password = request.form.get('password')
    confirm = request.form.get('confirm')

    if new_password or confirm:
        if new_password != confirm:
            return render_template('lab4/edit.html', user=user, error='Пароли не совпадают!')
        else:
            user['password'] = new_password

    user['login'] = new_login
    user['name'] = new_name

    session['login'] = new_login
    session['name'] = new_name

    return redirect('/lab4/users')