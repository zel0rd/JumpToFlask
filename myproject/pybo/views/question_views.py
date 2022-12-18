from ..db import db
from ..forms import QuestionForm, AnswerForm
from flask import Blueprint, render_template, request, url_for, redirect, flash, g
from datetime import datetime

from .auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question') 

@bp.route('/list')
def _list():
  question_list = {}
  cursor = db.cursor()
  number = 5;
  page = request.args.get('page', type=int, default=1)
  sql = "select q.id, q.subject, q.content, q.create_date, user.username from question as q left join user on q.user_id=user.id order by id ASC LIMIT {} OFFSET {};".format(number, number * (page-1))
  cursor.execute(sql)
  items = cursor.fetchall()
  
  sql =  "select count(*) as count from (select * from question order by id ASC LIMIT {} OFFSET {}) as R2;".format(number, number * page)
  cursor.execute(sql)
  next_count = cursor.fetchone()
  
  sql = "select count(*) as count from question;"
  cursor.execute(sql)
  get_length = cursor.fetchone()
  
  sql = "select question_id as id, count(question_id) as count from answer group by question_id;"
  cursor.execute(sql)
  answer_count = cursor.fetchall()
  
  answer_set = {}
  for data in answer_count:
    answer_set[data['id']] = data['count']

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
  question_list['number'] = number
  question_list['max_page'] = list(range(1,max_page+1))
  question_list['answer_set'] = answer_set
  
  return render_template('question/question_list.html', question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
  form = AnswerForm()
  cursor = db.cursor()
  sql = "select * from question left join user on question.user_id = user.id where question.id={}".format(question_id)
  cursor.execute(sql)
  question = cursor.fetchone()
  
  sql = "select * from answer left join user on answer.user_id=user.id where answer.question_id={}".format(question_id)
  cursor.execute(sql)
  answer_set = cursor.fetchall()
  
  return render_template('question/question_detail.html', question=question, answer_set=answer_set, form=form)

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
  form = QuestionForm()
  if request.method == "POST" and form.validate_on_submit():
    cursor = db.cursor()
    sql = "insert into question (subject, content, create_date, user_id) values ('{}','{}','{}',{})".format(form.subject.data, form.content.data, datetime.now(), g.user)
    cursor.execute(sql)
    db.commit()
    return redirect(url_for('main.index'))
  return render_template('question/question_form.html', form=form)


@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    cursor = db.cursor()
    sql = "select * from question where id={}".format(question_id)
    cursor.execute(sql)
    question = cursor.fetchone()
    print(question)
    if g.user != question['user_id']:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':  # POST 요청
        form = QuestionForm()
        if form.validate_on_submit():
            cursor = db.cursor()
            sql = "update question set subject='{}', content='{}', modify_date='{}' where id={};".format(form.subject.data, form.content.data, datetime.now(), question_id) 
            cursor.execute(sql)
            db.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:  # GET 요청
        form = QuestionForm(subject=question['subject'], content=question['content'])
    return render_template('question/question_form.html', form=form)
  
@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    cursor = db.cursor()
    sql = "select user.id as user_id from question left join user on question.user_id = user.id where question.id={}".format(question_id)
    cursor.execute(sql)
    question = cursor.fetchone()
    
    if g.user != question['user_id']:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    
    sql = "delete from question where id={}".format(question_id)
    cursor.execute(sql)
    db.commit()
    return redirect(url_for('question._list'))