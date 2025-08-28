# acolheMID/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_class="config.Config"):
  app = Flask(__name__)
  app.config.from_object(config_class)
  
  # Inicializar extensiones
  db.init_app(app)
  
  # Importar y Registrar blueprints(rutas)
  from app.routes import home_bp, auth_bp
  app.register_blueprint(home_bp)
  app.register_blueprint(auth_bp, url_prefix='/auth')
  return app