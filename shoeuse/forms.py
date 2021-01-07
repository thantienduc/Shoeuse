from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_mysqldb import MySQL
from shoeuse import mysql



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators =[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In') 


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    FName = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    MName = StringField('Midle Name')
    LName = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    BDate = StringField('Date of birth',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    Address = StringField('Address',
                           validators=[DataRequired(), Length(min=2, max=30)])
    Phone = StringField('Phone',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=20)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        cur = mysql.connection.cursor()
        user = cur.execute("SELECT Username FROM LogIn WHERE Username = %s", (username.data,))
        user = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        if user:
            raise ValidationError('That username has been already existed. Please choose different one!')
    
    def validate_email(self, email):
        cur = mysql.connection.cursor()
        user = cur.execute("SELECT Email FROM Client WHERE Email = %s",(email.data,))
        mysql.connection.commit()
        cur.close()
        if user:
            raise ValidationError('That email has been already existed. Please choose different one!')

class UndateAccount(FlaskForm):
    FName = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    MName = StringField('Midle Name')
    LName = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    Address = StringField('Address',
                           validators=[DataRequired(), Length(min=2, max=30)])
    Phone = StringField('Phone',
                           validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Update')

class PaymentForm(FlaskForm):
    Method = StringField('Payment Method',
                           validators=[DataRequired(), Length(min=2, max=30)])
    Discount = StringField('Discount')                    
    submit = SubmitField('Make Payment')
