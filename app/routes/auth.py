from flask import Blueprint, render_template

auth_bp = Blueprint("auth", __name__, template_folder='../templates/auth')

@auth_bp.route('/')
def auth():
  return 'Route auth'


@auth_bp.route('/signup')
def signup():
  return render_template('signup.html')

@auth_bp.route('/login')
def login():
  return render_template('login.html')