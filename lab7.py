from flask import Blueprint, render_template, request, abort, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)

def db_connect():
    if current_app.config.get('DB_TYPE') == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='ivan_starodubtsev_films',
            user='ivan_starodubtsev_films',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "films.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    cur.execute("SELECT id, title, title_ru, year, description FROM films ORDER BY id;")
    rows = cur.fetchall()
    films = [dict(row) for row in rows]
    db_close(conn, cur)
    return films


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    query = ("SELECT id, title, title_ru, year, description FROM films WHERE id=%s;"
             if current_app.config.get('DB_TYPE') == 'postgres'
             else "SELECT id, title, title_ru, year, description FROM films WHERE id=?;")
    cur.execute(query, (id,))
    film = cur.fetchone()
    db_close(conn, cur)

    if not film:
        abort(404)

    return dict(film)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()

    query = ("DELETE FROM films WHERE id=%s RETURNING id;"
             if current_app.config.get('DB_TYPE') == 'postgres'
             else "DELETE FROM films WHERE id=?;")

    cur.execute(query, (id,))
    deleted = cur.fetchone() if current_app.config.get('DB_TYPE') == 'postgres' else None

    if current_app.config.get('DB_TYPE') != 'postgres':
        if cur.rowcount == 0:
            db_close(conn, cur)
            return '', 404
        db_close(conn, cur)
        return '', 204

    db_close(conn, cur)

    if not deleted:
        return '', 404

    return '', 204


def validate_film(film):
    errors = {}

    if film.get('title') == '' and film.get('title_ru'):
        film['title'] = film['title_ru']

    if not film.get('title_ru', '').strip():
        errors['title_ru'] = 'Русское название обязательно'

    if not film.get('title', '').strip() and not film.get('title_ru', '').strip():
        errors['title'] = 'Введите хотя бы одно название'

    try:
        year = int(film.get('year', 0))
        if year < 1895 or year > 2025:
            errors['year'] = 'Год должен быть от 1895 до 2025'
    except:
        errors['year'] = 'Год должен быть числом'

    desc = film.get('description', '').strip()
    if not desc:
        errors['description'] = 'Описание обязательно'
    elif len(desc) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'

    return errors


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()

    errors = validate_film(film)
    if errors:
        return errors, 400

    conn, cur = db_connect()

    query = """
        UPDATE films
        SET title=%s, title_ru=%s, year=%s, description=%s
        WHERE id=%s
        RETURNING id, title, title_ru, year, description;
    """ if current_app.config.get('DB_TYPE') == 'postgres' else """
        UPDATE films
        SET title=?, title_ru=?, year=?, description=?
        WHERE id=?
    """

    cur.execute(query, (film['title'], film['title_ru'], film['year'], film['description'], id))

    if current_app.config.get('DB_TYPE') == 'postgres':
        updated = cur.fetchone()
        db_close(conn, cur)
        if not updated:
            return '', 404
        return dict(updated)
    else:
        count = cur.rowcount
        db_close(conn, cur)
        if count == 0:
            return '', 404
        return {
            "id": id,
            "title": film['title'],
            "title_ru": film['title_ru'],
            "year": film['year'],
            "description": film['description']
        }


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()

    errors = validate_film(film)
    if errors:
        return errors, 400

    conn, cur = db_connect()

    query = """
        INSERT INTO films (title, title_ru, year, description)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """ if current_app.config.get('DB_TYPE') == 'postgres' else """
        INSERT INTO films (title, title_ru, year, description)
        VALUES (?, ?, ?, ?);
    """

    cur.execute(query, (film['title'], film['title_ru'], film['year'], film['description']))

    if current_app.config.get('DB_TYPE') == 'postgres':
        new_id = cur.fetchone()['id']
    else:
        new_id = cur.lastrowid

    db_close(conn, cur)

    return str(new_id)
