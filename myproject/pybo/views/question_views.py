from ..db import db
from ..forms import QuestionForm, AnswerForm
from flask import Blueprint, render_template, request, url_for, redirect, flash
from datetime import datetime

bp = Blueprint('question', __name__, url_prefix='/question') 

@bp.route('/list')
def _list():
  cursor = db.cursor()
  sql = "SELECT * FROM `question`"
  cursor.execute(sql)
  question_list = cursor.fetchall()

  return render_template('question/question_list.html', question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
  form = AnswerForm()
  cursor = db.cursor()
  sql = "SELECT * FROM `question` WHERE id = {}".format(question_id)
  cursor.execute(sql)
  question = cursor.fetchone()
  
  sql = "SELECT * FROM `answer` WHERE question_id = {}".format(question_id)
  cursor.execute(sql)
  answer_set = cursor.fetchall()
  
  return render_template('question/question_detail.html', question=question, answer_set=answer_set, form=form)

@bp.route('/create/', methods=('GET', 'POST'))
def create():
  form = AnswerForm()
  if request.method == "POST" and form.validate_on_submit():
    cursor = db.cursor()
    content = request.form['content']
    sql = "insert into question (content, create_date) values ('{}','{}','{}')".format(content, datetime.now())
    cursor.execute(sql)
    db.commit()
    
    return redirect(url_for('question.detail', question_id=question_id))
  
  return render_template('question/question_form.html', form=form)
