from ..db import db
from datetime import datetime
from flask import Blueprint, render_template, url_for, redirect, request,g
from ..forms import QuestionForm, AnswerForm

from .auth_views import login_required

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>/', methods=('POST',))
@login_required
def create(question_id):
    form = AnswerForm()
    if form.validate_on_submit():
        cursor = db.cursor()
        content = request.form['content']
        sql = "insert into answer (question_id, content, create_date, user_id) values ({},'{}','{}',{})".format(question_id, content, datetime.now(), g.user)
        cursor.execute(sql)
        db.commit()
        
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('question/question_detail.html', form=form)