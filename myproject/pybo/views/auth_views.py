from flask import Blueprint, url_for, render_template, flash, request
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from ..db import db
from pybo.forms import UserCreateForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    cursor = db.cursor()
    if request.method == 'POST' and form.validate_on_submit():
        # user = User.query.filter_by(username=form.username.data).first()
        sql = "select * from user where username='{}'".format(form.username.data)
        print(sql)
        cursor.execute(sql)
        user = cursor.fetchone()
        print(user)
        if not user:
            sql = "insert into user (username, password, email) values ('{}','{}','{}');".format(form.username.data, generate_password_hash(form.password1.data), form.email.data)
            cursor.execute(sql)
            db.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)