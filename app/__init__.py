# acolheMID/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import Config
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()

def create_app(): #(config_class="config.Config")
  app = Flask(__name__)
  app.config.from_object(Config)#(config_class)
  
  # Inicializar extensiones
  db.init_app(app)
  migrate.init_app(app, db)
  csrf.init_app(app)
  
  # Inicializar Flask-Login
  login_manager.init_app(app)
  login_manager.login_view = 'auth.login'

  with app.app_context():
    from app.models import User, Post, Comment, Label
    db.create_all()
  
  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))


  # Importar y Registrar blueprints(rutas)
  from app.routes import home_bp, auth_bp
  app.register_blueprint(home_bp)
  app.register_blueprint(auth_bp, url_prefix='/auth')
  
  from . import routes
  
  return app