# acolheMid/config.py
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
  SECRET_KEY = os.environ.get("SECRET_KEY") or "MiaTa2026@modularCode!"
  
  # Leer variable de entorno para PostgreSQL o fallback a SQLite local
  uri = os.environ.get("DATABASE_URL")
  if uri and uri.startswith("postgres://"):
    # Render y Heroku usan postgres:// pero SQLAlchemy requiere postgresql://
    uri = uri.replace("postgres://", "postgresql://", 1)
  SQLALCHEMY_DATABASE_URI = uri or f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'app.db')}"
  
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  
  UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "uploads")
  MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # Max 2MB per img
  ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
