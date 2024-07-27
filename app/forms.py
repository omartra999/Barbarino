from flask_wtf import FlaskForm
from wtforms import StringField, TextField, EmailField, PasswordField, SubmitField, BooleanField, EmailField, IntegerField, DateFieldd
from datetime import datetime
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min= 3, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    birthday = DateField('Birthday', validators=[DataRequired(), validate_birthday])
    submit = SubmitField('Register')

    def validate_birthday(self, field):
        birthday = field.data
        today = datetime.today()
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
        if age < 16:
            raise ValidationError("You must be at least 18 years old.")


class AddressForm(FlaskForm):
    street = StringField('Street', validators=[DataRequired(), Length(min=5, max=100)])
    city = StringField('City', validators=[DataRequired(), Length(min=3, max=50)])
    plz = IntegerField('Plz', validators=[DataRequired(), Length(min=5, max=5)])
    houseNr = IntegerField('HouseNr', validators=[DataRequired()])
