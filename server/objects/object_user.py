from authentication.auth import *
from encryption.encrypt import *
from object_contact import *

class User():
    def __init__(self, login, phone, password, salt):
        self.login = login
        self.phone = phone
        self.password = password
        self.salt = salt
        self.secret_key = generate_2fa_secret()
        self.contacts = []

    def send_message():
        pass

    def receive_message():
        pass

    def addContact(self, contactUser: Contact):
        self.contacts.push(contactUser)
