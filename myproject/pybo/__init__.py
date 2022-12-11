from flask import Flask
from pymysql import cursors, connect
from .db import db

def create_app():
    app = Flask(__name__)

    # 블루프린트
    from .views import main_views, question_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    
    return app