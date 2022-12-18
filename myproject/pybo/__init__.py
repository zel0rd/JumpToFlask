import config
from .db import db
from flask import Flask
from pymysql import cursors, connect


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # 블루프린트
    from .views import main_views, question_views, answer_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    
    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    
    return app