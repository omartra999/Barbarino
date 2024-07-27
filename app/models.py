from mongoengine import ReferenceField,Document, StringField, DateField, DateTimeField, BooleanField,IntField
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(Document):

    first_name = StringField(required= True ,max_length=255)
    last_name = StringField(required= True ,max_length=255)
    username = StringField(required= True ,max_length=255, min_length= 5, unique= True)
    email = StringField(required= True ,max_length=255, unique= True)
    password = StringField(required= True ,max_length=255)
    birthday = DateField(required= True)
    address = ReferenceField(Address)
    created_at = DateTimeField(default=datetime.now)
    confirmed = BooleanField(required= True, default= False)


    def clean(self):
        self.email = self.email.lower()

        if self.birthday > datetime.now().date():
            raise ValidationError("Birthday cannot be in the future")
        elif not self.birthday or not self.username or not self.password or not self.first_name or not self.last_name or not self.email:
            raise ValidationError("All fields are required")
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @classmethod
    def find_by_email(cls, email):
        return cls.objects(email=email).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.objects(username=username).first()

    @classmethod
    def delete_by_email(cls, email):
        return cls.objects(email= email).delete()
    
    @classmethod
    def confirm_email(cls, email, confirmed):
        user = cls.find_by_email(email)
        if user:
            user.update(set__confirmed=confirmed)
            return True
        return False

    @classmethod
    def update_password(cls, email, password):
        user = cls.find_by_email(email)
        if user:
            user.update(set__password = set_password(password))
            return True
        return False

    @classmethod
    def update_first_name(cls, email, first_name):
        user = cls.find_by_email(email)
        if user:
            user.update(set__first_name=first_name)
            return True
        return False
    
    @classmethod
    def update_last_name(cls, email, last_name):
        user = cls.find_by_email(email)
        if user:
            user.update(set__last_name=last_name)
            return True
        return False

    @classmethod
    def update_email(cls, email, new_email):
        user = cls.find_by_email(email)
        if user:
            user.update(set__email=new_email)
            return True
        return False
    
    @classmethod
    def update_address(cls, email, new_address):
        user = cls.find_by_email(email)
        if user:
            user.update(set__address=new_address)
            return True
        return False

class Address(Document):
    street = StringField(required= True ,max_length=255)
    houseNr = IntField(required= True)
    plz = IntField(required= True)
    city = StringField(required= True ,max_length=255)
    country = StringField(required= True ,max_length=255)

    def clean(self):
        self.street = self.street.lower()
        self.city = self.city.lower()
        self.country = self.country.lower()

        if not self.street or not self.city or not self.country :
            raise ValidationError("all fields are required")

    