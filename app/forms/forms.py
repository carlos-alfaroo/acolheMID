from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, SelectField, FloatField, IntegerField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])
    submit = SubmitField('Post')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])    # INVESTIGAR Para que es Email()
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', 'Password must match')])

    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
    

class PostRol(FlaskForm):
    rol = SelectField('Rol', choices=[
        ('user', 'User'), 
        ('admin', 'Admin'), 
        ('editor', 'Editor'),
        ('ceo', 'Ceo')
    ])
    submit = SubmitField('Actualizar Rol')
    
    
    
    
    # class para agregar articulos al inventario
class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    category = StringField('Category', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Add Product') 
    
class AddToCartForm(FlaskForm):
    submit = SubmitField('Add to Cart')
'''    
class AddToInventoryForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Add to Inventory')
'''       