from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_pybo():
  return 'Hello, Pybo!'

@bp.route('/2')
def index():
  return 'Pybo index'