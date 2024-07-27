from flask import Flask, render_template, url_for, redirect, flash, request
from app.forms import RegistrationForm
from app.utlis import generate_token, verify_token
from app.models import User, Barber
from app import app, mail
from mongoengine import DoesNotExist, ValidationError, NotUniqueError
from flask_mail import Message
import yagmail

yag = yagmail.SMTP('omartra069@gmail.com', 'ioya kqxe iudb rfty')

@app.route('/register/user', methods=['POST', 'GET'])
def register_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Save data from form
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                email=form.email.data,
                birthday=form.birthday.data
            )
            # Hash password
            user.set_password(form.password.data)
            user.save()

            #Generate token to verify email
            token = generate_token(user.email)
            # Send email verification link
            verification_link = url_for('verify_email', token=token, _external=True)
            yag.send(to= user.email, subject='verification_link', contents=f'To verify your email, click the following link: {verification_link}')

            flash('A verification email has been sent to you. Please check your inbox.', 'success')
            return "<h1>Registration email sent</h1>"
        
        except ValidationError as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            if user.id:  # Check if user was saved to the database
                user.delete()
        except NotUniqueError as e:
            flash(f'Email or username already exists: {str(e)}', 'danger')
            if user.id:  # Check if user was saved to the database
                user.delete()
        except Exception as e:
            flash(f'An unexpected error occurred: {str(e)}', 'danger')
            if user.id:  # Check if user was saved to the database
                user.delete()
    return render_template('register.html', title='Register', form=form)

@app.route('/verify_email/<token>')
def verify_email(token):
    try:
        email = verify_token(token)
        if email:
            user = User.objects(email=email).first()
            if user:
                user.confirmed = True
                user.save()
                flash('Your email has been confirmed!', 'success')
                return "<h1>confirmed</h1>"
            else:
                flash('Invalid confirmation link.', 'warning')
        else:
            flash('The confirmation link is invalid or has expired.', 'warning')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
  # Redirect to home page or appropriate route
