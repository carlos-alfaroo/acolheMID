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
import cloudinary.uploader

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

inventory_bp = Blueprint("inventory", __name__, template_folder='../templates/inventory')
@inventory_bp.route('/')
@rol_required('admin', 'editor', 'ceo')
def dashboard_admin():
  count_users = User.query.count()
  total_users = count_users if count_users else 0
  
  products = Product.query.all()

  return render_template('dashboard_admin.html', total_users=total_users, products=products)


@inventory_bp.route('/add_product', methods=['GET', 'POST'])
@rol_required('admin', 'editor', 'ceo')
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
      filename = None
      
      # manejo de archivo
      if form.image.data:
        file = form.image.data
        try:
          # Subir a Cloudinary y obtener la URL
          upload_result = cloudinary.uploader.upload(file)
          filename = upload_result["secure_url"] # esta url se guarda en la DB
        except Exception as e:
          flash("Error al subir la imagen", "red")
          filename = None 
        
      new_product = Product(
          name=form.name.data,
          description=form.description.data,
          price=form.price.data,
          stock=form.stock.data,
          category=form.category.data,
          image=filename  # URL de Cloudinary
      )
      db.session.add(new_product)
      db.session.commit()
      flash(f'Producto {new_product.name} agregado al inventario', 'green')
      
    return render_template('add_product.html', form=form)
  
@inventory_bp.route('/search_products')
def search_products():
    query = request.args.get('query', '')
    results = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    return render_template('search_results.html', query=query, results=results)
  
@inventory_bp.route('/products_inventory')
def products_inventory():
    products = Product.query.all()
    return render_template('products_inventory.html', products=products)
  
@inventory_bp.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@rol_required('admin', 'editor', 'ceo')
def edit_product(id):
  product = Product.query.get_or_404(id)
  form = ProductForm(obj=product)
  
  if form.validate_on_submit():
    # solo sube imagen si una nueva es proporcionada
    if form.image.data and not isinstance(form.image.data, str):
        file = form.image.data
        if file.filename:  # Ensure it's not empty
          upload_result = cloudinary.uploader.upload(file)
          product.image = upload_result["secure_url"]
      
    product.name = form.name.data
    product.description = form.description.data
    product.price = form.price.data
    product.stock = form.stock.data
    product.category = form.category.data
      
    db.session.commit()
    flash(f'Producto {product.name} actualizado', 'green')
    return redirect(url_for('inventory.products_inventory'))
  
  return render_template('edit_product.html', form=form, product=product)

@inventory_bp.route('/delete_product/<int:id>', methods=['GET', 'POST'])
@rol_required('admin', 'editor', 'ceo')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash(f'Producto {product.name} eliminado', 'red')
    return redirect(url_for('inventory.products_inventory'))
  


@inventory_bp.route('/users_inventory')
@rol_required('admin', 'editor', 'ceo')
def users_inventory():
  users = User.query.all()
  return render_template('users_inventory.html', users=users)