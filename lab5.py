from flask import Blueprint, render_template, request, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'ivan_starodubtsev_knowledge_base',
            user = 'ivan_starodubtsev_knowledge_base',
            password = '123'
        )
        cur = conn.cursor(cursor_factory = RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab5.route('/lab5/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    name = request.form.get('name')

    if not (login and password and name):
        return render_template('lab5/register.html', error='Заполните все поля')
    
    conn, cur = db_connect()

    cur.execute("SELECT login FROM users WHERE login=%s;", (login, ))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html',
                               error="Такой пользователь уже существует!")
    
    password_hash = generate_password_hash(password)
    cur.execute("INSERT INTO users (login, password, name) VALUES (%s, %s, %s);", (login, password_hash, name))
    
    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/login.html', error="Заполните поля")
    
    conn, cur = db_connect()

    cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error="Логин и/или пароль неверны")
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error="Логин и/или пароль неверны")
    
    session['login'] = login

    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/create', methods = ['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == "GET":
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = bool(request.form.get('is_public'))

    if not title or not article_text:
        return render_template('lab5/create_article.html', error='Заполните все поля')

    conn, cur = db_connect()
    
    cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    login_id = cur.fetchone()["id"]

    cur.execute("INSERT INTO articles(user_id, title, article_text, is_public) VALUES (%s, %s, %s, %s);",
            (login_id, title, article_text, is_public))

    
    db_close(conn, cur)
    return redirect('/lab5')

@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    cur.execute("SELECT id FROM users WHERE login=%s;", (login, ))
    login_id = cur.fetchone()["id"]

    cur.execute("SELECT * FROM articles WHERE user_id=%s ORDER BY is_favorite DESC, id;", (login_id,))
    articles = cur.fetchall()

    if not articles:
        db_close(conn, cur)
        return render_template('/lab5/articles.html', articles=[], message='У вас нет статей')

    db_close(conn, cur)
    return render_template('/lab5/articles.html', articles=articles)

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5')

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
    article = cur.fetchone()

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article, error='Заполните все поля')

    cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s;", (title, article_text, article_id))
    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/users')
def users_list():
    conn, cur = db_connect()
    cur.execute("SELECT login, name FROM users;")
    users = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/users.html', users=users)

@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    user = cur.fetchone()

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user)

    name = request.form.get('name')
    password = request.form.get('password')
    confirm = request.form.get('confirm')

    if not name:
        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user, error='Имя не может быть пустым')

    if password:
        if password != confirm:
            db_close(conn, cur)
            return render_template('lab5/profile.html', user=user, error='Пароли не совпадают')
        password_hash = generate_password_hash(password)
        cur.execute("UPDATE users SET name=%s, password=%s WHERE login=%s;", (name, password_hash, login))
    else:
        cur.execute("UPDATE users SET name=%s WHERE login=%s;", (name, login))

    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/favorite/<int:article_id>')
def favorite(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    cur.execute("SELECT is_favorite FROM articles WHERE id=%s;", (article_id,))
    current = cur.fetchone()['is_favorite']
    cur.execute("UPDATE articles SET is_favorite=%s WHERE id=%s;", (not current, article_id))
    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/public')
def public_articles():
    conn, cur = db_connect()
    cur.execute("SELECT title, article_text FROM articles WHERE is_public=TRUE ORDER BY id DESC;")
    articles = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/public_articles.html', articles=articles)
