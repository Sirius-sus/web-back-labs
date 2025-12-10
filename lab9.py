from flask import Blueprint, render_template, request, jsonify, session, redirect
from db import db
from db.models import gift_box
from flask_login import current_user, login_required

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/')
def main():
    boxes = gift_box.query.all()
    unopened_count = gift_box.query.filter_by(is_opened=False).count()

    if 'opened_count' not in session:
        session['opened_count'] = 0

    return render_template('lab9/index.html',
                           boxes=boxes,
                           unopened_count=unopened_count)


@lab9.route('/lab9/open_box', methods=['POST'])
def open_box():
    data = request.get_json()
    box_id = data.get('box_id')

    box = gift_box.query.get(box_id)
    if not box:
        return jsonify({'error': 'not found'}), 404

    if box.auth_required and not current_user.is_authenticated:
        return jsonify({'auth_needed': True})

    if box.is_opened:
        return jsonify({'already_opened': True})

    if 'opened_count' not in session:
        session['opened_count'] = 0

    if session['opened_count'] >= 3:
        return jsonify({'limit_exceeded': True})

    box.is_opened = True
    db.session.commit()

    session['opened_count'] += 1

    return jsonify({'success': True,
                    'redirect_url': f'/lab9/congratulation/{box_id}'})


@lab9.route('/lab9/reset_boxes', methods=['POST'])
@login_required
def reset_boxes():
    db.session.query(gift_box).update({gift_box.is_opened: False})
    db.session.commit()
    session['opened_count'] = 0
    return jsonify({'success': True})


@lab9.route('/lab9/congratulation/<int:box_id>')
def congratulation(box_id):
    box = gift_box.query.get(box_id)
    img_path = f'/static/lab9/congratulation_{box_id}.jpg'
    return render_template('lab9/congratulation.html',
                           img_path=img_path,
                           message=box.message)
