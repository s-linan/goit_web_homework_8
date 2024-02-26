from mongoengine import Document, StringField, EmailField, BooleanField


class Contact(Document):
    full_name = StringField(required=True)
    email = EmailField(required=True)
    is_active = BooleanField(default=False)
