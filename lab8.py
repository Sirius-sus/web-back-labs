from flask import Blueprint, render_template, request, redirect, session, current_app
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy import or_
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html')

@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or login_form.strip() == '':
        return render_template('lab8/register.html',
                               error='Имя пользователя не должно быть пустым')

    if not password_form or password_form.strip() == '':
        return render_template('lab8/register.html',
                               error='Пароль не должен быть пустым')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html',
                               error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user, remember=False)

    return redirect('/lab8/')

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or login_form.strip() == '':
        return render_template('lab8/login.html',
                               error='Логин не должен быть пустым')

    if not password_form or password_form.strip() == '':
        return render_template('lab8/login.html',
                               error='Пароль не должен быть пустым')

    user = users.query.filter_by(login=login_form).first()

    remember_me = True if request.form.get('remember') else False

    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=remember_me)
        return redirect('/lab8/')

    return render_template('lab8/login.html',
                           error='Ошибка входа: логин и/или пароль неверны')

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = bool(request.form.get('is_public'))

    if not title or not article_text:
        return render_template('lab8/create_article.html', error='Заполните все поля')

    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=article_text,
        is_public=is_public,
        is_favorite=False,
        likes=0,
    )

    db.session.add(new_article)
    db.session.commit()

    return redirect('/lab8/articles')

@lab8.route('/lab8/articles')
@login_required
def article_list():
    user_articles = articles.query.filter_by(login_id=current_user.id)\
                                  .order_by(articles.id).all()

    if not user_articles:
        return render_template('lab8/articles.html', articles=[], message='У вас нет статей')

    return render_template('lab8/articles.html', articles=user_articles)

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()

    if not article:
        return redirect('/lab8/articles')

    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        return render_template('lab8/edit_article.html',
                               article=article,
                               error='Заполните все поля')

    article.title = title
    article.article_text = article_text

    db.session.commit()

    return redirect('/lab8/articles')

@lab8.route('/lab8/delete/<int:article_id>')
@login_required
def delete_article(article_id):
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()

    if not article:
        return redirect('/lab8/articles')

    db.session.delete(article)
    db.session.commit()

    return redirect('/lab8/articles')

@lab8.route('/lab8/public')
def public_articles():
    public_articles = articles.query.filter_by(is_public=True).order_by(articles.id.desc()).all()
    return render_template('lab8/public_articles.html', articles=public_articles)

@lab8.route('/lab8/search', methods=['GET', 'POST'])
def search():
    query = None
    results = []

    if request.method == 'POST':
        query = request.form.get('query')

        if query:
            pattern = f"%{query}%"

            if current_user.is_authenticated:
                results = articles.query.filter(
                    or_(
                        articles.title.ilike(pattern),
                        articles.article_text.ilike(pattern)
                    ),
                    or_(
                        articles.is_public == True,
                        articles.login_id == current_user.id
                    )
                ).all()
            else:
                results = articles.query.filter(
                    or_(
                        articles.title.ilike(pattern),
                        articles.article_text.ilike(pattern)
                    ),
                    articles.is_public == True
                ).all()

    return render_template('lab8/search.html', results=results, query=query)