# acolheMID/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import Config
from flask_login import LoginManager, current_user
from sqlalchemy import func
import cloudinary

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
  
  # Inicializar Cloudinary desde variable de entorno
  cloudinary.config(cloudinary_url=app.config["CLOUDINARY_URL"])
  
  # Inicializar Flask-Login
  login_manager.init_app(app)
  login_manager.login_view = 'auth.login'

  with app.app_context():
    from app.models import User, Post, Comment, Label, Product, CartItem
    db.create_all()
  
  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))

# Este context processor hace que `cart_count` esté disponible en todas las templates
  @app.context_processor
  def inject_cart_count():
    if current_user.is_authenticated:
      # Suma de cantidades de todos los productos en el carrito del usuario
      cart_count = db.session.query(func.sum(CartItem.quantity)).filter_by(user_id=current_user.id).scalar() or 0
    else:
      cart_count = 0
    return dict(cart_count=cart_count)


  # Importar y Registrar blueprints(rutas)
  from app.routes import home_bp, auth_bp, cart_bp, inventory_bp
  app.register_blueprint(home_bp)
  app.register_blueprint(auth_bp, url_prefix='/auth')
  app.register_blueprint(cart_bp, url_prefix='/cart')
  app.register_blueprint(inventory_bp, url_prefix='/inventory')
  
  from . import routes
  
  return app