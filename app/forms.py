from flask_wtf import FlaskForm
from wtforms import StringField,  EmailField, PasswordField, SubmitField, BooleanField, EmailField, IntegerField, DateField, SelectField, RadioField
from datetime import datetime
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError,Optional, Length

##Forms for HTML are defined here


class RegistrationForm(FlaskForm):
    user_type = RadioField('Register as', choices=[('user', 'User'), ('barber', 'Barber')], default='user', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    phone_number = StringField('Phone Number', validators=[Optional(DataRequired)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    birthday = DateField('Birthday', validators=[DataRequired()])
    
    # Additional fields for Barber registration and address
    profile_picture = StringField('Profile Picture')
    buisness_name = StringField('buisness Name', validators= [Optional(DataRequired)])
    bio = StringField('Bio', validators=[Length(max=200)])
    street = StringField('Street')
    city = StringField('City')
    plz = StringField('Zip Code')

    submit = SubmitField('Register')

    def validate_birthday(self, field):
        birthday = field.data
        today = datetime.today()
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
        if age < 16:
            raise ValidationError("You must be at least 18 years old.")

