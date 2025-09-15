import os
import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename
from app import db
from app.forms.forms import SignUpForm, LoginForm, PostRol, ProductForm
from app.models import User, CartItem, Product
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from app.utils.decorators import rol_required


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

inventory_bp = Blueprint("inventory", __name__, template_folder='../templates/inventory')
@inventory_bp.route('/')
def dashboard_admin():
  count_users = User.query.count()
  total_users = count_users if count_users else 0
  return render_template('dashboard_admin.html', total_users=total_users)


@inventory_bp.route('/add_product', methods=['GET', 'POST'])
@rol_required('admin', 'editor', 'ceo')
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
      filename = None
      
      # manejo de archivo
      if form.image.data:
        file = form.image.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        
      new_product = Product(
          name=form.name.data,
          description=form.description.data,
          price=form.price.data,
          stock=form.stock.data,
          category=form.category.data,
          image=filename
      )
      db.session.add(new_product)
      db.session.commit()
      flash(f'Producto {new_product.name} agregado al inventario', 'green')
      
    return render_template('add_product.html', form=form)
