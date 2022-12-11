import sys
sys.path.append('../pybo')

from flask import Blueprint, render_template
from pybo.db import db


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
  cursor = db.cursor()
  sql = "SELECT * FROM `question` WHERE id = {}".format(question_id)
  cursor.execute(sql)
  question = cursor.fetchone()

  return render_template('question/question_detail.html', question=question)