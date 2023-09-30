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
        self.received_messages = []
        self.sended_messages = []
        self.contacts = []

    def addSendedMessage(self, message: Message):
        self.sended_messages.append(message)

    def addReceivedMessage(self, message: Message):
        self.received_messages.append(message)

    def addContact(self, contactUser: Contact):
        self.contacts.push(contactUser)
