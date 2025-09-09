from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user

def rol_required(*roles):
  """
    Decorador para restringir acceso a usuarios con ciertos roles.
    Uso: @rol_required('admin', 'editor')
    """
  def wrapper(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
      if not current_user.is_authenticated:
        flash("Debes iniciar sesión primero.", "red")
        return redirect(url_for('auth.login'))
      if current_user.rol not in roles:
        flash("No tienes permiso para acceder a esta página.", "red")
        return redirect(url_for('auth.dashboard'))
      return f(*args, **kwargs)
    return decorated_function
  return wrapper
  