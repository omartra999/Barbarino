from itsdangerous import URLSafeTimedSerializer
from flask import current_app, url_for, render_template, flash
import traceback
from app import yag

def generate_token(email):
    """
    Generate a time-sensitive token for email verification.
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

def verify_token(token, expiration=3600):
    """
    Verify the token and return the email if the token is valid and not expired.
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except (SignatureExpired, BadSignature) as e:
        # Handle token expiration or invalid signature
        return None
    return email

def send_verification_email(user, subject, token):
            try:
                verification_link = url_for('verify_email', token=token, _external=True)
                html_content = render_template('verification_email.html', username=user.username, verification_link=verification_link)
                yag.send(to= user.email, subject='verification_link', contents= html_content)

                flash('A verification email has been sent to you. Please check your inbox.', 'success')
                return "<h1>Registration email sent</h1>"
            except Exception as e:
                    print(f"Failed to send verification email to {user.email}: {str(e)}")
                    if user.id:  # Check if user was saved to the database
                     user.delete()
                    traceback.print_exc()
    