from itsdangerous import URLSafeTimedSerializer
from flask import current_app

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
