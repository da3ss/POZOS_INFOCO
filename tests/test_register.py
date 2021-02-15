
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 

db = SQLAlchemy()

def create_app():
    app = Flask(__name__,template_folder='../templates')

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from ..models import User

    @login_manager.user_loader
    def load_user(user_id):
        
        return User.query.get(int(user_id))

    
    from ..auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    
    from ..app import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

app=create_app()

class BluePrintTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
   
    def signup(self, email, name, password):
        return self.app.post('/signup',data=dict(email=email, name=name, password=password),follow_redirects=True)

    def test_valid_user_signup(self):
        response = self.signup('info@inpt.a', 'infoc_inp', 'infoco')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
