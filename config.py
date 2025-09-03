# acolheMid/config.py
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
  SECRET_KEY = os.environ.get("SECRET_KEY") or "default_secret_key"
  SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'app.db')}" #os.environ.get("DATABASE_URL") or "sqlite:///site.db"
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "uploads")
  MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # Max 2MB per img
  ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}