from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=6, max=12)])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label = 'Register')

class LoginForm(FlaskForm):
    username_login = StringField(label='Username', validators=[DataRequired()])
    password_login = PasswordField(label='Password', validators=[DataRequired()])
    login = SubmitField(label='Login')

class InputForm(FlaskForm):
    sepal_length = FloatField('Sepal Length', [DataRequired()], default=5.2)
    sepal_width = FloatField('Sepal Width', [DataRequired()], default=3.6)
    petal_length = FloatField('Petal length', [DataRequired()], default=1.8)
    petal_width = FloatField('Petal Width', [DataRequired()], default=0.2)
    send = SubmitField('Send')


