from datetime import datetime
#from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin


# Tabla intermedia para N:M entre Post y Label
post_label = db.Table('post_label',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('label_id', db.Integer, db.ForeignKey('labels.id'))
)

class User(UserMixin, db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  username = db.Column(db.String(30), unique=True, nullable=False)
  email = db.Column(db.String(30), unique=True, nullable=False)
  password = db.Column(db.String(200), nullable=False)
  bio = db.Column(db.String(200))
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  rol = db.Column(db.String(20), default="user")  # Roles: user, admin, editor
  #last_login = 

  posts = db.relationship('Post', back_populates='user', lazy=True)
  comments = db.relationship('Comment', back_populates='user', lazy=True)
  
  def set_password(self, password):
    self.password = generate_password_hash(password) #method='sha256')
  
  def check_password(self, password):
    return check_password_hash(self.password, password)
  
  def has_rol(self, *roles):
    return self.rol in roles

class Post(UserMixin, db.Model):
  __tablename__ = 'posts'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  content = db.Column(db.Text, nullable=False)
  category = db.Column(db.String(50))
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
  status = db.Column(db.String(20), default="published")
  
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  user = db.relationship('User', back_populates='posts')

  comments = db.relationship("Comment", back_populates="post", lazy=True)
  labels = db.relationship("Label", secondary=post_label, back_populates="posts")

class Comment(UserMixin, db.Model):
  __tablename__ = 'comments'
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

  post = db.relationship('Post', back_populates='comments')
  user = db.relationship('User', back_populates='comments') #diferencias entre esta y la de arriba

class Label(UserMixin, db.Model):
  __tablename__ = 'labels'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)

  posts = db.relationship("Post", secondary=post_label, back_populates="labels")




