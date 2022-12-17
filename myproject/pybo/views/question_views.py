from ..db import db
from ..forms import QuestionForm, AnswerForm
from flask import Blueprint, render_template, request, url_for, redirect, flash
from datetime import datetime

bp = Blueprint('question', __name__, url_prefix='/question') 

@bp.route('/list')
def _list():
  question_list = {}
  cursor = db.cursor()
  number = 5;
  page = request.args.get('page', type=int, default=1)
  sql = "select * from question order by id ASC LIMIT {} OFFSET {};".format(number, number * (page-1))
  cursor.execute(sql)
  items = cursor.fetchall()
  
  sql =  "select count(*) as count from (select * from question order by id ASC LIMIT {} OFFSET {}) as R2;".format(number, number * page)
  cursor.execute(sql)
  next_count = cursor.fetchone()
  
  sql = "select count(*) as count from question;"
  cursor.execute(sql)
  get_length = cursor.fetchone()
  
  next_num = page + 1
  prev_num = page - 1
  has_next = bool(next_count['count'] > 0)
  has_prev = bool(page > 1)
  max_page = (get_length['count'] - 1) // number + 1
  
  question_list['item'] = items
  question_list['page'] = page
  question_list['has_next'] = has_next
  question_list['has_prev'] = has_prev
  question_list['next_num'] = next_num
  question_list['prev_num'] = prev_num
  question_list['max_page'] = list(range(1,max_page+1))
  
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
  form = QuestionForm()
  if request.method == "POST" and form.validate_on_submit():
    cursor = db.cursor()
    sql = "insert into question (subject, content, create_date) values ('{}','{}','{}')".format(form.subject.data, form.content.data, datetime.now())
    cursor.execute(sql)
    db.commit()
    return redirect(url_for('main.index'))
  return render_template('question/question_form.html', form=form)
