from itsdangerous import URLSafeTimedSerializer
from flask import current_app, url_for, render_template
from app import app
import traceback
import yagmail

yag = yagmail.SMTP(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

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
    """
    Send a verification email to the specified email address.
    """
    try:
        verification_link = url_for('verify_email', token=token, _external=True)
        html_content = render_template('verification_email.html', username=user.username, verification_link=verification_link)
        yag.send(to= user.email, subject='verification_link', contents= html_content)
    except Exception as e:
        # Handle email sending failure
        print(f"Failed to send verification email to {user.email}: {str(e)}")
        traceback.print_exc()
        return False