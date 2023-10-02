from authentication.auth import *
from encryption.encrypt import *

class Message():
    def __init__(self, text, sender, receiver, tag = None, nonce = None):
        self.text = text
        self.receiver = receiver
        self.sender = sender
        self.tag = tag
        self.nonce = nonce

class User():
    def __init__(self, login, phone, password, salt):
        self.login = login
        self.phone = phone
        self.password = password
        self.salt = salt
        self.secret_key = generate_2fa_secret()
        self.received_messages = []
        self.sended_messages = []

    def addSendedMessage(self, message: Message):
        self.sended_messages.append(message)

    def addReceivedMessage(self, message: Message):
        self.received_messages.append(message)
