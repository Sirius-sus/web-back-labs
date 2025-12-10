from flask import Blueprint, render_template, request, redirect
from flask_login import login_user, login_required, current_user, logout_user
from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from db.models import cell_booking, users

rgz = Blueprint('rgz', __name__)

@rgz.route('/rgz/')
def main():
    cells = cell_booking.query.order_by(cell_booking.cell_number).all()

    if current_user.is_authenticated:
        user_cells = [c.cell_number for c in cells if c.tenant_id == current_user.id]
    else:
        user_cells = []

    busy_count = sum(1 for c in cells if c.tenant_id is not None)
    free_count = 100 - busy_count

    return render_template(
        "rgz/index.html",
        cells=cells,
        user_cells=user_cells,
        busy_count=busy_count,
        free_count=free_count,
        show_alert=False
    )


@rgz.route('/rgz/book/<int:cell>')
def book(cell):
    booking = cell_booking.query.get(cell)
    if not booking:
        return render_main_with_alert("Ячейка не существует")

    # Если ячейка занята 
    if booking.tenant_id is not None:
        tenant = users.query.get(booking.tenant_id)
        login = tenant.login if tenant else "неизвестно"
        return render_main_with_alert(f"Эта ячейка занята пользователем: {login}")

    # Если пользователь не авторизован
    if not current_user.is_authenticated:
        return render_main_with_alert("Для бронирования необходимо войти в систему")

    # Проверка лимита 5 ячеек
    if cell_booking.query.filter_by(tenant_id=current_user.id).count() >= 5:
        return render_main_with_alert("Вы не можете бронировать больше пяти ячеек")

    # Бронирование
    booking.tenant_id = current_user.id
    db.session.commit()

    return main()


@rgz.route('/rgz/release/<int:cell>')
def release(cell):
    booking = cell_booking.query.get(cell)

    if not current_user.is_authenticated:
        return render_main_with_alert("Необходима авторизация")

    if booking.tenant_id != current_user.id:
        return render_main_with_alert("Вы не можете освободить чужую ячейку")

    booking.tenant_id = None
    db.session.commit()

    return main()


def render_main_with_alert(message):
    cells = cell_booking.query.order_by(cell_booking.cell_number).all()

    if current_user.is_authenticated:
        user_cells = [c.cell_number for c in cells if c.tenant_id == current_user.id]
    else:
        user_cells = []

    busy_count = sum(1 for c in cells if c.tenant_id is not None)
    free_count = 100 - busy_count

    return render_template(
        'rgz/index.html',
        cells=cells,
        user_cells=user_cells,
        busy_count=busy_count,
        free_count=free_count,
        show_alert=True,
        alert_message=message
    )

@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rgz/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or login_form.strip() == '':
        return render_template('rgz/register.html',
                               error='Имя пользователя не должно быть пустым')

    if not password_form or password_form.strip() == '':
        return render_template('rgz/register.html',
                               error='Пароль не должен быть пустым')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('rgz/register.html',
                               error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user, remember=False)

    return redirect('/rgz/')

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or login_form.strip() == '':
        return render_template('rgz/login.html',
                               error='Логин не должен быть пустым')

    if not password_form or password_form.strip() == '':
        return render_template('rgz/login.html',
                               error='Пароль не должен быть пустым')

    user = users.query.filter_by(login=login_form).first()

    remember_me = True if request.form.get('remember') else False

    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=remember_me)
        return redirect('/rgz/')

    return render_template('rgz/login.html',
                           error='Ошибка входа: логин и/или пароль неверны')

@rgz.route('/rgz/logout')
@login_required
def logout():
    logout_user()
    return redirect('/rgz/')