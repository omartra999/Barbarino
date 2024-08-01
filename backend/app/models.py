from mongoengine import ReferenceField,Document, StringField, DateField, DateTimeField, BooleanField,IntField, ListField, FloatField
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


#Address Model for Database
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

    

#User Model for Database with all functions related to users like changing passowrd, updating info and hashing password.
class User(Document):

    first_name = StringField(required= True ,max_length=255)
    last_name = StringField(required= True ,max_length=255)
    username = StringField(required= True ,max_length=255, min_length= 5, unique= True)
    email = StringField(required= True ,max_length=255, unique= True)
    password = StringField(required= True ,max_length=255)
    birthday = DateField(required= True)
    address = ReferenceField('Address')
    profile_picture = StringField()
    phone_number = StringField(max_length= 15)
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
    
    def confirm_email(self,):
            user.update(set__confirmed=True)

#Barber Model for Database with barber functions like rating, adding a bio etc...
class Barber(Document):

    username = StringField(required=True, unique=True, max_length=50)
    first_name = StringField(required=True, max_length=50)
    last_name = StringField(required=True, max_length=50)
    buisness_name = StringField( max_length= 50)
    email = StringField(required=True, unique=True, max_length=100)
    password = StringField(required=True, max_length=255)
    birthday = DateTimeField(required=True)
    profile_picture = StringField() 
    phone_number = StringField(max_length=15)
    bio = StringField(max_length=200, default='')
    address = ReferenceField(Address)
    available_slots = ListField(StringField()) 
    confirmed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    average_rating = FloatField(default=0.0)
    rating_count = IntField(default = 0)

    def add_rating(self, rating):
        if 0<= rating <= 5:
            total_rating = self.average_rating * self.rating_count
            self.rating_count +=  1
            self.average_rating = (total_rating + rating) / self.rating_count
            self.save()

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
    

    def confirm_email(self):
        user.update(set__confirmed=True)


