from flask import Flask
from pymysql import cursors, connect

db = connect(host='localhost',
            user='root',
            password='qhdkscjfwj0!',
            database='pybo')

def create_app():
    app = Flask(__name__)

    # 블루프린트
    from .views import main_views
    app.register_blueprint(main_views.bp)
    
    @app.route('/')
    def hello():
        cursor = db.cursor()
        sql = "SELECT * FROM `answer`"
        
        cursor.execute(sql)
        result = cursor.fetchone()
        
        print(result)
        return str(result)
    
    return app