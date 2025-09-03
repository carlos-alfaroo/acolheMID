import os
import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename
from app import db
from app.forms.forms import SignUpForm, LoginForm
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint("auth", __name__, template_folder='../templates/auth')

@auth_bp.route('/')
def auth():
  return 'Route auth'


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignUpForm()
  if form.validate_on_submit():
    if User.query.filter_by(email=form.email.data).first() or User.query.filter_by(username=form.username.data).first():
      flash('¡El usuario ya existe!', 'red')
    else:
      new_user = User(username=form.username.data, 
                  email=form.email.data, 
                  password=form.password.data)
      new_user.set_password(form.password.data)
      try:  
        db.session.add(new_user)
        db.session.commit()
      except IntegrityError:
        db.session.rollback()
      flash('Registro exitoso. Inicia sesión.', 'green')
      return render_template('login.html', form=form)
  return render_template('signup.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user and user.check_password(form.password.data):
      login_user(user)
      flash('Login successful!', 'green')
      return render_template('dashboard.html', form=form)
      
    flash('Invalid username or password', 'red')
    return render_template('login.html', form=form)
  return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
  logout_user()
  flash('Logout successful', 'yellow')
  return render_template('login.html', form=LoginForm())

@auth_bp.route('/dashboard')
@login_required
def dashboard():
  return render_template('dashboard.html')