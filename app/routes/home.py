from flask import Blueprint, render_template, url_for

home_bp = Blueprint("home", __name__, template_folder="../templates/home")

@home_bp.route('/')
def home():
  return render_template('home.html')

@home_bp.route('/carrito')
def carrito():
  return render_template('carrito.html')