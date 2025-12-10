from flask import Blueprint, render_template

rgz = Blueprint('rgz', __name__)

@rgz.route('/rgz/')
def main():
    return render_template('rgz/index.html')