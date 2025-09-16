import os
import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from werkzeug.utils import secure_filename
from app import db
from app.forms.forms import SignUpForm, LoginForm, PostRol, ProductForm, AddToCartForm
from app.models import User, CartItem, Product
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from app.utils.decorators import rol_required
import stripe


cart_bp = Blueprint("cart", __name__, template_folder='../templates/cart')

@cart_bp.route('/')
def home():
  products = Product.query.all()
  return render_template('products.html', products=products)

@cart_bp.route('/shop')
def shop():
  form = AddToCartForm()
  products = Product.query.all()
  return render_template('products.html', products=products, form=form)

@cart_bp.route('/cart')
def view_cart():
  form = AddToCartForm()
  cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
  total_price = sum(item.product.price * item.quantity for item in cart_items)
  return render_template('view_cart.html', cart_items=cart_items, total_price=total_price, form=form)



@cart_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
  form = AddToCartForm()
  product = Product.query.get_or_404(product_id)

  if form.validate_on_submit():
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product.id).first()
    if cart_item:
      if cart_item.quantity < product.stock:
        cart_item.quantity += 1
        db.session.commit()
        product_name = product.name or "Producto"
        flash(f"{product_name} agregado al carrito", "green")
      else: 
        flash(f"No hay más stock disponible de {product.name}", "red")
    else:
      if product.stock > 0:
        cart_item = CartItem(user_id=current_user.id, product_id=product.id, quantity=1)
        db.session.add(cart_item)
        db.session.commit()
        product_name = product.name or "Producto"
        flash(f"{product_name} agregado al carrito", "green")
      else:
        flash(f"{product.name} está agotado", "red")
  else:
    flash('Error al agregar al carrito', 'red')

  #return render_template('products.html', product=product, form=form)
  return redirect(url_for('cart.shop'))





@cart_bp.route('/update_quantity/<int:item_id>', methods=['POST'])
@login_required
def update_quantity(item_id):
  form = AddToCartForm()
  item = CartItem.query.get_or_404(item_id)

  if item.user_id != current_user.id:
    flash('No tienes permiso para modificar este item', 'red')
    return redirect(url_for('cart.view_cart'))
  
  action = request.form.get('action')
  
  if action == 'increase':
    if item.quantity < item.product.stock:
      item.quantity += 1
    else:
      flash("No hay más unidades disponibles", "red")
  elif action == 'decrease':
    item.quantity -= 1
    if item.quantity <= 0:
      db.session.delete(item)
      db.session.commit()
      flash('Item eliminado del carrito', 'yellow')
  
  db.session.commit()
  return redirect(url_for('cart.view_cart'))




@cart_bp.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        return jsonify({'error': 'No hay productos en el carrito'}), 400

    for item in cart_items:
      if item.quantity > item.product.stock:
        return jsonify({'error': f'No hay suficiente stock para el producto {item.product.name}'}), 400

    line_items = []
    for item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'mxn',
                'product_data': {'name': item.product.name},
                'unit_amount': int(item.product.price * 100),
            },
            'quantity': item.quantity,
        })

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=url_for('cart.success', _external=True),
            cancel_url=url_for('cart.cancel', _external=True),
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@cart_bp.route('/success')
@login_required
def success():
  cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
  
  for item in cart_items:
    if item.product.stock >= item.quantity:
      item.product.stock -= item.quantity
    else:
      flash(f"Erro: stock insuficiente para {item.product.name}", "red")
      return redirect(url_for('cart.view_cart'))
    
  # Vaciar carrito después de actualizar inventario
  CartItem.query.filter_by(user_id=current_user.id).delete()
  db.session.commit()
  
  flash('Pago exitoso ✅! Gracias por tu compra.', 'green')
  return render_template('success.html')

@cart_bp.route('/cancel')
@login_required
def cancel():
  flash('Pago cancelado ❌. Puedes intentar de nuevo.', 'yellow')
  return redirect(url_for('cart.view_cart'))
