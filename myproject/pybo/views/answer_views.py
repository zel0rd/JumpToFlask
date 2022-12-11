import sys
from datetime import datetime
from flask import Blueprint, render_template, url_for, redirect, request

sys.path.append('../pybo')
from pybo.db import db

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>/', methods=('POST',))
def create(question_id):
    cursor = db.cursor()
    sql = "insert into answer (question_id, content, create_date) values ({},{},{})".format(question_id, request.form['content'], datetime.now())
    cursor.execute(sql)
    result = cursor.fetchall()
    
    return redirect(url_for('question.detail', question_id=question_id))
